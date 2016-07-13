from anillo.http import responses

from core.ideas import idea_entities, idea_actions

from tools.adt.converter import to_plain, from_plain

from web.handler import Handler

from web.decorators import login_required


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
        # TODO validate body
        title = request.body["title"]
        description = request.body["description"]
        is_public = request.body["is_public"]

        idea = idea_actions.create_idea(
            request.user,
            idea_entities.IdeaForCreate(
                title = title,
                description = description,
                is_public = is_public,
            )
        )

        return responses.Ok(to_plain(idea, ignore_fields=["id"]))

