# -*- coding: utf-8 -*-

from sqlalchemy import Column, String
from sqlalchemy.sql import select
from sqlalchemy.dialects.postgresql import ARRAY

from core.projects import project_entities

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
        projects = repo.retrieve_adts(
            context,
            project_entities.Project,
            select([repo.projects]).order_by("title")
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
