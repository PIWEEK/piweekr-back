# -*- coding: utf-8 -*-

import arrow
import uuid

from services.repository.sql.projects import project_repository
from services.repository.sql.users import user_repository

from core import exceptions

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


def get_project(project_uuid):
    return project_repository.retrieve_by_uuid(project_uuid)


#######################################
## Interesteds
#######################################

def add_interested_user(project, interested_user):
    interested = project_repository.retrieve_interested(project.id, interested_user.id)
    if interested:
        raise exceptions.InconsistentData("User {} was already interested to the project".format(interested_user.username))

    project_repository.create_interested(
        project_entities.ProjectInterested(
            project_id = project.id,
            user_id = interested_user.id,
        )
    )

def list_interested(project):
    return project_repository.retrieve_interested_list(project.id)


def remove_interested_user(project, interested_user):
    interested = project_repository.retrieve_interested(project.id, interested_user.id)
    if not interested:
        raise exceptions.InconsistentData("User {} was not interested to the project".format(interested_user.username))

    project_repository.delete_interested(interested)


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

    comment = project_repository.create_comment(comment)
    return project_repository.retrieve_comment(comment.id)


def list_comments(project):
    comments = project_repository.retrieve_comment_list(project)
    return comments


#######################################
## Reaction
#######################################

def create_reaction(owner, project, reaction_for_create):
    reaction = project_entities.ProjectReaction(
        uuid = uuid.uuid4().hex,
        code = reaction_for_create.code,
        owner_id = owner.id,
        project_id = project.id,
        created_at = arrow.now(),
    )

    project.increase_reaction_count(reaction.code)
    project_repository.update(project)

    reaction = project_repository.create_reaction(reaction)
    return project_repository.retrieve_reaction(reaction.id)


def list_reactions(project):
    reactions = project_repository.retrieve_reaction_list(project)
    return reactions

