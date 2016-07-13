# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy.sql import select, join
from sqlalchemy.dialects.postgresql import JSONB

from core.ideas import idea_entities
from core.users import user_entities

from services.repository.sql import repo

repo.add_adt_table(
    idea_entities.Idea,
    "ideas",
    manual_columns={
        "reactions_counts": Column("reactions_counts", JSONB),
    }
)

repo.add_adt_table(
    idea_entities.IdeaInvited,
    "ideas_invited",
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
        idea = repo.retrieve_single_adt(context,
            idea_entities.Idea,
            select([repo.ideas])
                .where(repo.ideas.c.uuid == idea_uuid)
        )
    return idea


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

