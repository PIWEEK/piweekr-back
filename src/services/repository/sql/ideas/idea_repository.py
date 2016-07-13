# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy.sql import select
from sqlalchemy.dialects.postgresql import JSONB

from core.ideas import idea_entities
from core.users import user_entities

from services.repository.sql import repo


#######################################
## Idea
#######################################

repo.add_adt_table(
    idea_entities.Idea,
    "ideas",
    manual_columns={
        "reactions_counts": Column("reactions_counts", JSONB),
    }
)


def create(idea):
    with repo.context() as context:
        idea = repo.insert_adt(context, repo.ideas, idea)
    return idea


def list():
    with repo.context() as context:
        ideas = repo.retrieve_joined_adts(
            context,
            idea_entities.Idea,
            {"ideas": idea_entities.Idea, "users": user_entities.User},
            select(
                [repo.ideas, repo.users],
                use_labels=True
            )
            .select_from(
                repo.ideas.join(
                    repo.users,
                    repo.ideas.c.owner_id == repo.users.c.id
                )
            ).order_by(repo.ideas.c.title)
        )
    return ideas


def retrieve_by_uuid(idea_uuid):
    with repo.context() as context:
        idea = repo.retrieve_single_adt(
            context,
            idea_entities.Idea,
            select(
                [repo.ideas]
            ).where(
                repo.ideas.c.uuid == idea_uuid
            )
        )
    return idea


#######################################
## Inviteds
#######################################

repo.add_adt_table(
    idea_entities.IdeaInvited,
    "ideas_invited",
)


def create_invited(idea_invited):
    with repo.context() as context:
        idea = repo.insert_adt(context, repo.ideas_invited, idea_invited)
    return idea_invited


def retrieve_invited_list(idea_id):
    with repo.context() as context:
        invited = repo.retrieve_joined_adts(
            context,
            idea_entities.IdeaInvited,
            {"ideas_invited": idea_entities.IdeaInvited, "users": user_entities.User},
            select(
                [repo.ideas_invited, repo.users],
                use_labels=True
            ).select_from(
                repo.ideas_invited.join(
                    repo.users,
                    repo.ideas_invited.c.user_id == repo.users.c.id
                )
            ).where(
                repo.ideas_invited.c.idea_id == idea_id
            ).order_by(repo.users.c.full_name)
        )
    return invited


#######################################
## Coment
#######################################

repo.add_adt_table(
    idea_entities.IdeaComment,
    "idea_comments",
)


def create_comment(new_comment):
    with repo.context() as context:
        comment = repo.insert_adt(context, repo.idea_comments, new_comment)
    return comment


def retrieve_comment_list(idea):
    with repo.context() as context:
        comments = repo.retrieve_joined_adts(
            context,
            idea_entities.IdeaComment,
            {"idea_comments": idea_entities.IdeaComment,
             "ideas": idea_entities.Idea,
             "users": user_entities.User},
            select(
                [repo.idea_comments, repo.ideas, repo.users],
                use_labels=True
            )
            .select_from(
                repo.idea_comments.join(
                    repo.ideas,
                    repo.idea_comments.c.idea_id == repo.ideas.c.id
                )
                .join(
                    repo.users,
                    repo.idea_comments.c.owner_id == repo.users.c.id
                )
            ).where(
                repo.idea_comments.c.idea_id == idea.id
            ).order_by(repo.idea_comments.c.created_at)
        )
    return comments
