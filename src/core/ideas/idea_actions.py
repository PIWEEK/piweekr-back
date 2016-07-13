from tools.password import generate_hash, verify_hash
from services.repository.sql.ideas import idea_repository
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
        title = idea_for_create.title,
        description = idea_for_create.description,
        owner_id = owner.id,
        created_at = arrow.now(),
        is_public = idea_for_create.is_public,
        forked_from = None,
        comments_count = 0,
        reactions_counts = {},
    )
    return idea_repository.create(idea)


def update_idea(owner, idea):
    return idea_repository.update(idea)


def list_ideas():
    return idea_repository.list()


def get_idea(idea_uuid):
    return idea_repository.retrieve_by_uuid(idea_uuid)


#######################################
## Inviteds
#######################################

def invite_users(user, idea, invited_users):
    if idea.owner_id != user.id:
        raise exceptions.Forbidden("Only owner can invite users")
    if idea.is_public:
        raise exceptions.InconsistentData("Only private ideas can have invited users")

    for user_name in invited_users:
        invited_user = user_repository.retrieve_by_user_name(user_name)
        if not invited_user:
            raise exceptions.InconsistentData("Can't find user {}".format(user_name))
        if invited_user.id == user.id:
            raise exceptions.InconsistentData("You cannot invite yourself to the idea")

        idea_repository.create_invited(
            idea_entities.IdeaInvited(
                idea_id = idea.id,
                user_id = invited_user.id,
            )
        )

def list_invited(idea):
    return idea_repository.retrieve_invited_list(idea.id)


#######################################
## Coment
#######################################

def create_comment(owner, idea,  comment_for_create):
    if not idea.is_public or idea.owner_id != owner.id:
        invited = idea_repository.retrieve_invited_by_user_id(owner.id)
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

    return idea_repository.create_comment(comment)


def list_comments(idea):
    comments = idea_repository.retrieve_comment_list(idea)
    return comments
