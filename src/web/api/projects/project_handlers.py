from anillo.http import responses

from core.projects import project_actions

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
                    "idea_from": {"ignore_fields": ["id", "is_active", "owner_id", "forked_from", "comments_count",
                                               "reactions_counts"]}
                }
            )
            for project in projects
        ])


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
