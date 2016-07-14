from copy import deepcopy
from tools.password import generate_hash, verify_hash
from services.repository.sql.ideas import idea_repository
from services.repository.sql.projects import project_repository
from services.repository.sql.users import user_repository

from core import exceptions

from . import idea_entities

import uuid
import arrow


#######################################
## Idea
#######################################

def create_idea(owner, idea_for_create):
    idea = idea_entities.Idea(
        uuid = uuid.uuid4().hex,
        is_active = True,
        title = idea_for_create.title,
        description = idea_for_create.description,
        owner_id = owner.id,
        created_at = arrow.now(),
        is_public = idea_for_create.is_public,
        forked_from_id = None,
        comments_count = 0,
        reactions_counts = {},
    )
    idea = idea_repository.create(idea)

    if idea_for_create.invited_usernames:
        if idea.is_public:
            raise exceptions.InconsistentData("Only private ideas can have invited users")
        for invited_username in idea_for_create.invited_usernames:
            invited_user = user_repository.retrieve_by_username(invited_username)
            if not invited_user:
                raise exceptions.InconsistentData("Can't find user {}".format(invited_username))
            if invited_user.id == idea.owner_id:
                raise exceptions.InconsistentData("You cannot invite yourself to the idea")
            idea_repository.create_invited(
                idea_entities.IdeaInvited(
                    idea_id = idea.id,
                    user_id = invited_user.id,
                )
            )

    return idea_repository.retrieve_by_uuid(idea.uuid)


def update_idea(idea, updates):
    data = deepcopy(updates.to_dict())
    idea.edit(data)
    idea_repository.update(idea)
    return idea_repository.retrieve_by_uuid(idea.uuid)


def list_ideas(user):
    return idea_repository.list_for_user(user)


def get_idea(idea_uuid):
    return idea_repository.retrieve_by_uuid(idea_uuid)


def fork_idea(user, idea):
    if idea.owner_id == user.id:
        raise exceptions.Forbidden("You cannot fork your own idea")

    forked_idea = idea_entities.Idea(
        uuid = uuid.uuid4().hex,
        is_active = True,
        title = idea.title,
        description = idea.description,
        owner_id = user.id,
        created_at = arrow.now(),
        is_public = idea.is_public,
        forked_from_id = idea.id,
        comments_count = 0,
        reactions_counts = {},
    )
    forked_idea = idea_repository.create(forked_idea)

    return idea_repository.retrieve_by_uuid(forked_idea.uuid)


def promote_idea(user, idea):
    if idea.owner_id != user.id:
        raise exceptions.Forbidden("Only owner can promote an idea")

    idea.deactivate()
    idea_repository.update(idea)

    from core.projects import project_entities
    project = project_entities.Project(
        uuid = uuid.uuid4().hex,
        title = idea.title,
        description = idea.description,
        technologies = [],
        needs = "",
        logo = "",
        piweek_id = 1, # TODO
        idea_from_id = idea.id,
        owner_id = idea.owner_id,
        created_at = arrow.utcnow(),
        comments_count=0,
        reactions_counts={}
    )

    from services.repository.sql.projects import project_repository
    project = project_repository.create(project)

    for invited in idea_repository.retrieve_invited_list(idea.id):
        project_repository.create_interested(
            project_entities.ProjectInterested(
                project_id = project.id,
                user_id = invited.user_id,
            )
        )
    return project_repository.retrieve_by_uuid(project.uuid)


#######################################
## Inviteds
#######################################

def invite_users(user, idea, invited_usernames):
    if idea.owner_id != user.id:
        raise exceptions.Forbidden("Only owner can invite users")
    if idea.is_public:
        raise exceptions.InconsistentData("Only private ideas can have invited users")

    for invited_username in invited_usernames:
        invited_user = user_repository.retrieve_by_username(invited_username)
        if not invited_user:
            raise exceptions.InconsistentData("Can't find user {}".format(invited_username))
        if invited_user.id == user.id:
            raise exceptions.InconsistentData("You cannot invite yourself to the idea")
        invited = idea_repository.retrieve_invited(idea.id, invited_user.id)
        if invited:
            raise exceptions.InconsistentData("User {} was already invited to the idea".format(invited_username))

        idea_repository.create_invited(
            idea_entities.IdeaInvited(
                idea_id = idea.id,
                user_id = invited_user.id,
            )
        )

def list_invited(idea):
    return idea_repository.retrieve_invited_list(idea.id)


def remove_invited_user(user, idea, invited_username):
    if idea.owner_id != user.id:
        raise exceptions.Forbidden("Only owner can invite users")
    if idea.is_public:
        raise exceptions.InconsistentData("Only private ideas can have invited users")

    invited_user = user_repository.retrieve_by_username(invited_username)
    if not invited_user:
        raise exceptions.InconsistentData("Can't find user {}".format(invited_username))

    invited = idea_repository.retrieve_invited(idea.id, invited_user.id)
    if not invited:
        raise exceptions.InconsistentData("User {} was not invited to the idea".format(invited_username))

    idea_repository.delete_invited(invited)


#######################################
## Comment
#######################################

def create_comment(owner, idea, comment_for_create):
    if not idea.is_public and idea.owner_id != owner.id:
        invited = idea_repository.retrieve_invited(idea.id, owner.id)
        if not invited:
            raise exceptions.Forbidden("Only invited users can comment")

    comment = idea_entities.IdeaComment(
        uuid = uuid.uuid4().hex,
        content = comment_for_create.content,
        owner_id = owner.id,
        idea_id = idea.id,
        created_at = arrow.now(),
    )

    idea.increase_comment_count()
    idea_repository.update(idea)

    comment = idea_repository.create_comment(comment)
    return idea_repository.retrieve_comment(comment.id)


def list_comments(idea):
    comments = idea_repository.retrieve_comment_list(idea)
    return comments


#######################################
## Reaction
#######################################

def create_reaction(owner, idea, reaction_for_create):
    if not idea.is_public and idea.owner_id != owner.id:
        invited = idea_repository.retrieve_invited(idea.id, owner.id)
        if not invited:
            raise exceptions.Forbidden("Only invited users can react")

    reaction = idea_entities.IdeaReaction(
        uuid = uuid.uuid4().hex,
        code = reaction_for_create.code,
        owner_id = owner.id,
        idea_id = idea.id,
        created_at = arrow.now(),
    )

    idea.increase_reaction_count(reaction.code)
    idea_repository.update(idea)

    reaction = idea_repository.create_reaction(reaction)
    return idea_repository.retrieve_reaction(reaction.id)


def list_reactions(idea):
    reactions = idea_repository.retrieve_reaction_list(idea)
    return reactions

