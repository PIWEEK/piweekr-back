from copy import deepcopy
from tools.password import generate_hash, verify_hash
from services.repository.sql.ideas import idea_repository
from services.repository.sql.projects import project_repository
from services.repository.sql.users import user_repository

from . import idea_entities

import uuid
import arrow


#######################################
## Idea
#######################################

def create_idea(owner, idea_for_create):
    """
    pre:
        not idea_for_create.invited_users or not idea_for_create.is_public
        not idea_for_create.invited_users or forall(idea_for_create.invited_users, lambda u: u.id != owner.id)
    """
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

    if idea_for_create.invited_users:
        for invited_user in idea_for_create.invited_users:
            idea_repository.create_invited(
                idea_entities.IdeaInvited(
                    idea_id = idea.id,
                    user_id = invited_user.id,
                )
            )

    return idea_repository.retrieve_by_uuid(idea.uuid)


def update_idea(owner, idea, idea_for_update):
    """
    pre:
        idea.owner_id == owner.id
    """
    idea.edit(idea_for_update)
    idea_repository.update(idea)
    return idea_repository.retrieve_by_uuid(idea.uuid)


def list_ideas(user):
    return idea_repository.list_for_user(user)


def get_idea(idea_uuid):
    return idea_repository.retrieve_by_uuid(idea_uuid)


def fork_idea(user, idea):
    """
    pre:
        idea.owner_id != user.id
    """
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
    """
    pre:
        idea.owner_id != user.id
    """
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

def invite_users(user, idea, invited_users):
    """
    pre:
        idea.owner_id == user.id
        idea.is_public == False
        forall(invited_users, lambda u: u.id != user.id)
        forall(invited_users, lambda u: get_invited(idea, u) == None)
    """
    for invited_user in invited_users:
        idea_repository.create_invited(
            idea_entities.IdeaInvited(
                idea_id = idea.id,
                user_id = invited_user.id,
            )
        )


def get_invited(idea, user):
    return idea_repository.retrieve_invited(idea.id, user.id)


def list_invited(idea):
    return idea_repository.retrieve_invited_list(idea.id)


def remove_invited_user(user, idea, invited):
    """
    pre:
        idea.owner_id == user.id
        idea.is_public == False
    """
    idea_repository.delete_invited(invited)


#######################################
## Comment
#######################################

def create_comment(user, idea, comment_for_create):
    """
    pre:
        idea.is_public or idea.owner_id == user.id or get_invited(idea, user) != None
    """
    comment = idea_entities.IdeaComment(
        uuid = uuid.uuid4().hex,
        content = comment_for_create.content,
        owner_id = user.id,
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
    """
    pre:
        idea.is_public or idea.owner_id == user.id or get_invited(idea, user) != None
    """
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

