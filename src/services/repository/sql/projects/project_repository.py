# -*- coding: utf-8 -*-

from sqlalchemy import Column, String
from sqlalchemy.sql import select, join
from sqlalchemy.dialects.postgresql import ARRAY, JSONB

from core.projects import project_entities
from core.ideas import idea_entities
from core.users import user_entities

from services.repository.sql import repo


#######################################
## Projects
#######################################

repo.add_adt_table(
    project_entities.Project,
    "projects",
    manual_columns={
        "technologies": Column("technologies", ARRAY(String)),
        "reactions_counts": Column("reactions_counts", JSONB),
    }
)


def create(project):
    with repo.context() as context:
        project = repo.insert_adt(context, repo.projects, project)
    return project


def update(project):
    with repo.context() as context:
        project = repo.update_adt(context, repo.projects, project)
    return project


def list():
    with repo.context() as context:
        projects = repo.retrieve_joined_adts(
            context,
            project_entities.Project,
            {"projects": project_entities.Project, "users": user_entities.User, "ideas": idea_entities.Idea},
            select(
                [repo.projects, repo.users, repo.ideas],
                use_labels=True
            ).select_from(
                repo.projects.join(
                    repo.users,
                    repo.projects.c.owner_id == repo.users.c.id
                ).join(
                    repo.ideas,
                    repo.projects.c.idea_from_id == repo.ideas.c.id
                )
            ).order_by(repo.projects.c.title)
        )
        for project in projects:
            interested = repo.retrieve_joined_adts(
                context,
                project_entities.ProjectInterested,
                {"projects_interested": project_entities.ProjectInterested, "users": user_entities.User},
                select(
                    [repo.projects_interested, repo.users],
                    use_labels=True
                ).select_from(
                    repo.projects_interested.join(
                        repo.users,
                        repo.projects_interested.c.user_id == repo.users.c.id
                    )
                ).where(
                    repo.projects_interested.c.project_id == project.id
                ).order_by(repo.users.c.full_name)
            )
            participant = repo.retrieve_joined_adts(
                context,
                project_entities.ProjectParticipant,
                {"projects_participant": project_entities.ProjectParticipant, "users": user_entities.User},
                select(
                    [repo.projects_participant, repo.users],
                    use_labels=True
                ).select_from(
                    repo.projects_participant.join(
                        repo.users,
                        repo.projects_participant.c.user_id == repo.users.c.id
                    )
                ).where(
                    repo.projects_participant.c.project_id == project.id
                ).order_by(repo.users.c.full_name)
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


#######################################
## Interesteds
#######################################

repo.add_adt_table(
    project_entities.ProjectInterested,
    "projects_interested",
)


def create_interested(project_interested):
    with repo.context() as context:
        project = repo.insert_adt(context, repo.projects_interested, project_interested)
    return project_interested


def retrieve_interested_list(project_id):
    with repo.context() as context:
        interested = repo.retrieve_joined_adts(
            context,
            project_entities.ProjectInterested,
            {"projects_interested": project_entities.ProjectInterested, "users": user_entities.User},
            select(
                [repo.projects_interested, repo.users],
                use_labels=True
            ).select_from(
                repo.projects_interested.join(
                    repo.users,
                    repo.projects_interested.c.user_id == repo.users.c.id
                )
            ).where(
                repo.projects_interested.c.project_id == project_id
            ).order_by(repo.users.c.full_name)
        )
    return interested


def retrieve_interested(project_id, user_id):
    with repo.context() as context:
        interested = repo.retrieve_single_adt(
            context,
            project_entities.ProjectInterested,
            select(
                [repo.projects_interested]
            ).where(
                (repo.projects_interested.c.project_id == project_id) &
                (repo.projects_interested.c.user_id == user_id)
            )
        )
    return interested


def delete_interested(interested):
    with repo.context() as context:
        row_count = repo.delete_adt(context, repo.projects_interested, interested)
        return row_count


#######################################
## Participants
#######################################

repo.add_adt_table(
    project_entities.ProjectParticipant,
    "projects_participant",
)


def create_participant(project_participant):
    with repo.context() as context:
        project = repo.insert_adt(context, repo.projects_participant, project_participant)
    return project_participant


def retrieve_participant_list(project_id):
    with repo.context() as context:
        participants = repo.retrieve_joined_adts(
            context,
            project_entities.ProjectParticipant,
            {"projects_participant": project_entities.ProjectParticipant, "users": user_entities.User},
            select(
                [repo.projects_participant, repo.users],
                use_labels=True
            ).select_from(
                repo.projects_participant.join(
                    repo.users,
                    repo.projects_participant.c.user_id == repo.users.c.id
                )
            ).where(
                repo.projects_participant.c.project_id == project_id
            ).order_by(repo.users.c.full_name)
        )
    return participants


def retrieve_participant(project_id, user_id):
    with repo.context() as context:
        participant = repo.retrieve_single_adt(
            context,
            project_entities.ProjectParticipant,
            select(
                [repo.projects_participant]
            ).where(
                (repo.projects_participant.c.project_id == project_id) &
                (repo.projects_participant.c.user_id == user_id)
            )
        )
    return participant


def delete_participant(participant):
    with repo.context() as context:
        row_count = repo.delete_adt(context, repo.projects_participant, participant)
        return row_count


#######################################
## Comment
#######################################

repo.add_adt_table(
    project_entities.ProjectComment,
    "project_comments",
)


def create_comment(new_comment):
    with repo.context() as context:
        comment = repo.insert_adt(context, repo.project_comments, new_comment)
    return comment


def retrieve_comment_list(project):
    with repo.context() as context:
        comments = repo.retrieve_joined_adts(
            context,
            project_entities.ProjectComment,
            {"project_comments": project_entities.ProjectComment,
             "projects": project_entities.Project,
             "users": user_entities.User},
            select(
                [repo.project_comments, repo.projects, repo.users],
                use_labels=True
            ).select_from(
                repo.project_comments.join(
                    repo.projects,
                    repo.project_comments.c.project_id == repo.projects.c.id
                )
                .join(
                    repo.users,
                    repo.project_comments.c.owner_id == repo.users.c.id
                )
            ).where(
                repo.project_comments.c.project_id == project.id
            ).order_by(repo.project_comments.c.created_at)
        )
    return comments


def retrieve_comment(comment_id):
    with repo.context() as context:
        comment = repo.retrieve_single_joined_adt(
            context,
            project_entities.ProjectComment,
            {"project_comments": project_entities.ProjectComment,
             "projects": project_entities.Project,
             "users": user_entities.User},
            select(
                [repo.project_comments, repo.projects, repo.users],
                use_labels=True
            ).select_from(
                repo.project_comments.join(
                    repo.projects,
                    repo.project_comments.c.project_id == repo.projects.c.id
                )
                .join(
                    repo.users,
                    repo.project_comments.c.owner_id == repo.users.c.id
                )
            ).where(
                repo.project_comments.c.id == comment_id
            )
        )
    return comment


#######################################
## Reaction
#######################################

repo.add_adt_table(
    project_entities.ProjectReaction,
    "project_reactions",
)


def create_reaction(new_reaction):
    with repo.context() as context:
        reaction = repo.insert_adt(context, repo.project_reactions, new_reaction)
    return reaction


def retrieve_reaction_list(project):
    with repo.context() as context:
        reactions = repo.retrieve_joined_adts(
            context,
            project_entities.ProjectReaction,
            {"project_reactions": project_entities.ProjectReaction,
             "projects": project_entities.Project,
             "users": user_entities.User},
            select(
                [repo.project_reactions, repo.projects, repo.users],
                use_labels=True
            ).select_from(
                repo.project_reactions.join(
                    repo.projects,
                    repo.project_reactions.c.project_id == repo.projects.c.id
                )
                .join(
                    repo.users,
                    repo.project_reactions.c.owner_id == repo.users.c.id
                )
            ).where(
                repo.project_reactions.c.project_id == project.id
            ).order_by(repo.project_reactions.c.created_at)
        )
    return reactions


def retrieve_reaction(reaction_id):
    with repo.context() as context:
        reaction = repo.retrieve_single_joined_adt(
            context,
            project_entities.ProjectReaction,
            {"project_reactions": project_entities.ProjectReaction,
             "projects": project_entities.Project,
             "users": user_entities.User},
            select(
                [repo.project_reactions, repo.projects, repo.users],
                use_labels=True
            ).select_from(
                repo.project_reactions.join(
                    repo.projects,
                    repo.project_reactions.c.project_id == repo.projects.c.id
                )
                .join(
                    repo.users,
                    repo.project_reactions.c.owner_id == repo.users.c.id
                )
            ).where(
                repo.project_reactions.c.id == reaction_id
            )
        )
    return reaction


def retrieve_reaction_of_user(project_id, user_id):
    with repo.context() as context:
        reaction = repo.retrieve_single_adt(
            context,
            project_entities.ProjectReaction,
            select(
                [repo.project_reactions]
            ).where(
                (repo.project_reactions.c.project_id == project_id) &
                (repo.project_reactions.c.owner_id == user_id)
            )
        )
    return reaction


def delete_reaction(reaction):
    with repo.context() as context:
        row_count = repo.delete_adt(context, repo.project_reactions, reaction)
        return row_count

