from anillo.http import responses

from core.projects import project_actions
from core.projects import project_entities

from tools.adt.converter import to_plain, from_plain

from web.handler import Handler
from web.decorators import login_required


#######################################
## Project
#######################################

class ProjectsList(Handler):
    def get(self, request):
        projects = project_actions.list_projects()
        return responses.Ok([
            to_plain(project, ignore_fields=["id"],
                relationships = {
                    "owner": {"ignore_fields": ["id", "password"]},
                    "idea_from": {"ignore_fields": ["id", "is_active", "owner_id", "forked_from_id",
                                                    "comments_count", "reactions_counts"]},
                    "users_interested": {
                        "ignore_fields": ["id"],
                        "relationships": {
                            "user": {"ignore_fields": ["id", "password"]},
                        }
                    },
                    "users_participant": {
                        "ignore_fields": ["id"],
                        "relationships": {
                            "user": {"ignore_fields": ["id", "password"]},
                        }
                    }
                }
            )
            for project in projects
        ])


class ProjectDetail(Handler):
    def get(self, request, project_uuid):
        project = project_actions.get_project(project_uuid)
        if not project:
            return responses.NotFound()

        return responses.Ok(to_plain(project, ignore_fields=["id"]))

    def put(self, request):
        raise NotImplementedError("TODO")

    def delete(self, request):
        raise NotImplementedError("TODO")


#######################################
## Interested
#######################################

class ProjectInterestedList(Handler):
    def get(self, request, project_uuid):
        project = project_actions.get_project(project_uuid)
        if not project:
            return responses.NotFound()

        interested_list = project_actions.list_interested(project)
        return responses.Ok([
            to_plain(interested, ignore_fields=["id", "project_id"],
                relationships = {
                    "user": {"ignore_fields": ["id", "password"]},
                }
            )
            for interested in interested_list
        ])

    @login_required
    def post(self, request, project_uuid):
        project = project_actions.get_project(project_uuid)
        if not project:
            return responses.NotFound()

        project_actions.add_interested_user(project, request.user)
        return responses.Ok()

    @login_required
    def delete(self, request, project_uuid):
        project = project_actions.get_project(project_uuid)
        if not project:
            return responses.NotFound()

        project_actions.remove_interested_user(project, request.user)
        return responses.Ok()


#######################################
## Participants
#######################################

class ProjectParticipantsList(Handler):
    def get(self, request, project_uuid):
        project = project_actions.get_project(project_uuid)
        if not project:
            return responses.NotFound()

        participant_list = project_actions.list_participant(project)
        return responses.Ok([
            to_plain(participant, ignore_fields=["id", "project_id"],
                relationships = {
                    "user": {"ignore_fields": ["id", "password"]},
                }
            )
            for participant in participant_list
        ])

    @login_required
    def post(self, request, project_uuid):
        project = project_actions.get_project(project_uuid)
        if not project:
            return responses.NotFound()

        project_actions.add_participant_user(project, request.user)
        return responses.Ok()

    @login_required
    def delete(self, request, project_uuid):
        project = project_actions.get_project(project_uuid)
        if not project:
            return responses.NotFound()

        project_actions.remove_participant_user(project, request.user)
        return responses.Ok()


#######################################
## Comment
#######################################

class ProjectCommentsList(Handler):
    def get(self, request, project_uuid):
        project = project_actions.get_project(project_uuid)
        if not project:
            return responses.NotFound()

        comments = project_actions.list_comments(project)
        return responses.Ok([
            to_plain(comment, ignore_fields=["id"],
                relationships = {
                    "owner": {"ignore_fields": ["id", "password"]},
                }
            )
            for comment in comments
        ])

    @login_required
    def post(self, request, project_uuid):
        project = project_actions.get_project(project_uuid)
        if not project:
            return responses.NotFound()

        validator = project_entities.ProjectCommentForCreateValidator(request.body)
        if validator.is_valid():
            comment = project_actions.create_comment(
                request.user,
                project,
                project_entities.ProjectCommentForCreate(**validator.cleaned_data)
            )
            return responses.Ok(to_plain(
                comment,
                ignore_fields=["id"],
                relationships = {
                    "owner": {"ignore_fields": ["id", "password"]},
                }
            ))
        else:
            return responses.BadRequest(validator.errors)

    @login_required
    def delete(self, request, project_uuid):
        raise NotImplementedError("TODO")


#######################################
## Reaction
#######################################

class ProjectReactionsList(Handler):
    def get(self, request, project_uuid):
        project = project_actions.get_project(project_uuid)
        if not project:
            return responses.NotFound()

        reactions = project_actions.list_reactions(project)
        return responses.Ok([
            to_plain(reaction, ignore_fields=["id"],
                relationships = {
                    "owner": {"ignore_fields": ["id", "password"]},
                }
            )
            for reaction in reactions
        ])

    @login_required
    def post(self, request, project_uuid):
        project = project_actions.get_project(project_uuid)
        if not project:
            return responses.NotFound()

        validator = project_entities.ProjectReactionForCreateValidator(request.body)
        if validator.is_valid():
            reaction = project_actions.create_reaction(
                request.user,
                project,
                project_entities.ProjectReactionForCreate(**validator.cleaned_data)
            )
            return responses.Ok(to_plain(
                reaction,
                ignore_fields=["id"],
                relationships = {
                    "owner": {"ignore_fields": ["id", "password"]},
                }
            ))
        else:
            return responses.BadRequest(validator.errors)

    @login_required
    def delete(self, request, project_uuid):
        raise NotImplementedError("TODO")
