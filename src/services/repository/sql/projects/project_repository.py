# -*- coding: utf-8 -*-

from sqlalchemy import Column, String
from sqlalchemy.sql import select, join
from sqlalchemy.dialects.postgresql import ARRAY

from core.projects import project_entities
from core.users import user_entities

from services.repository.sql import repo


repo.add_adt_table(
    project_entities.Project,
    "projects",
    manual_columns={
        "technologies": Column("technologies", ARRAY(String)),
    }
)


def create(project):
    with repo.context() as context:
        project = repo.insert_adt(context, repo.projects, project)
    return project


def list():
    with repo.context() as context:
        projects = repo.retrieve_joined_adts(
            context,
            project_entities.Project,
            {"projects": project_entities.Project, "users": user_entities.User},
            select(
                [repo.projects, repo.users],
                use_labels=True
            ).select_from(
                join(
                    repo.projects,
                    repo.users,
                    repo.projects.c.owner_id == repo.users.c.id
                )
            ).order_by(repo.projects.c.title)
        )
    return projects


def retrieve_by_uuid(uuid):
    with repo.context() as context:
        project = repo.retrieve_single_adt(
            context,
            project_entities.Project,
            select([repo.projects]).where(repo.projects.c.uuid == uuid)
        )
    return project


def retrieve_by_title(title):
    with repo.context() as context:
        project = repo.retrieve_single_adt(
            context,
            project_entities.Project,
            select([repo.projects]).where(repo.projects.c.title == title)
        )
    return project
