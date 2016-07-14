# -*- coding: utf-8 -*-

import arrow

from services.repository.sql.projects import project_repository

from . import project_entities


#######################################
## Projects
#######################################

def create_new_project(project_for_create):
    project = project_entities.Project(
        uuid = uuid.uuid4().hex,
        title = project_for_create.title,
        description = project_for_create.description,
        technologies = project_for_create.technologies,
        needs = project_for_create.needs,
        logo = project_for_create.logo,
        piweek_id = project_for_create.piweek_id,
        idea_from_id = project_for_create.idea_from_id,
        owner_id = project_for_create.owner_id,
        created_at = arrow.utcnow(),
        comments_count=0,
        reactions_counts={}
    )

    return project_repository.create(project)


def list_projects():
    projects = project_repository.list()
    return projects


#######################################
## Comments
#######################################

def create_comment(owner, project,  comment_for_create):
    comment = project_entities.ProjectComment(
        uuid = uuid.uuid4().hex,
        content = comment_for_create.content,
        owner_id = owner.id,
        project_id = project.id,
        created_at = arrow.now(),
    )

    project.increase_comment_count()
    project_repository.update(project)

    return project_repository.create_comment(comment)


def list_comments(project):
    comments = project_repository.retrieve_comment_list(project)
    return comments
