# -*- coding: utf-8 -*-

import arrow

from services.repository.sql.projects import project_repository

from . import project_entities


def create_new_project(project_for_create):
    project = project_entities.Project(
        title = project_for_create.title,
        description = project_for_create.description,
        technologies = project_for_create.technologies,
        needs = project_for_create.needs,
        logo = project_for_create.logo,
        piweek_id = project_for_create.piweek_id,
        idea_from_id = project_for_create.idea_from_id,
        owner_id = project_for_create.owner_id,
        created_at = arrow.utcnow()
        comments_count=0,
        reactions_counts={},
    )

    return project_repository.create(project)


def list_projects():
    projects = project_repository.list()
    return projects
