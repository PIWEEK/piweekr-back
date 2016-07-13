from anillo.http import responses

from core.ideas import idea_entities, idea_actions

from tools.adt.converter import to_plain, from_plain

from web.handler import Handler
from web.decorators import login_required


#######################################
## Idea
#######################################

class IdeasList(Handler):
    def get(self, request):
        ideas = idea_actions.list_ideas()
        return responses.Ok([
            to_plain(idea, ignore_fields=["id"],
                relationships = {
                    "owner": {"ignore_fields": ["id", "password"]},
                }
            )
            for idea in ideas
        ])

    @login_required
    def post(self, request):
        validator = idea_entities.IdeaForCreateValidator(request.body)
        if validator.is_valid():
            idea = idea_actions.create_idea(
                request.user,
                idea_entities.IdeaForCreate(**validator.cleaned_data)
            )
            return responses.Ok(to_plain(idea, ignore_fields=["id"]))
        else:
            return responses.BadRequest(validator.errors)


class IdeaDetail(Handler):
    def get(self, request, idea_uuid):
        idea = idea_actions.get_idea(idea_uuid)
        if not idea:
            return responses.NotFound()

        return responses.Ok(to_plain(idea, ignore_fields=["id"]))

    def put(self, request):
        raise NotImplementedError("TODO")

    def delete(self, request):
        raise NotImplementedError("TODO")


#######################################
## Invited
#######################################

class IdeaInvitedList(Handler):
    def get(self, request, idea_uuid):
        idea = idea_actions.get_idea(idea_uuid)
        if not idea:
            return responses.NotFound()

        invited_list = idea_actions.list_invited(idea)
        return responses.Ok([
            to_plain(invited, ignore_fields=["id", "idea_id"],
                relationships = {
                    "user": {"ignore_fields": ["id", "password"]},
                }
            )
            for invited in invited_list
        ])

    def post(self, request, idea_uuid):
        raise NotImplementedError("TODO")

    def delete(self, request, idea_uuid):
        raise NotImplementedError("TODO")


#######################################
## Coment
#######################################

class IdeaComentsList(Handler):
    def get(self, request, idea_uuid):
        idea = idea_actions.get_idea(idea_uuid)
        if not idea:
            return responses.NotFound()

        comments = idea_actions.list_comments(idea)
        return responses.Ok([
            to_plain(comment, ignore_fields=["id"],
                relationships = {
                    "owner": {"ignore_fields": ["id", "password"]},
                }
            )
            for comment in comments
        ])

    @login_required
    def post(self, request, idea_uuid):
        raise NotImplementedError("TODO")

    @login_required
    def delete(self, request, idea_uuid):
        raise NotImplementedError("TODO")
