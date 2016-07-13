from anillo.http import responses

from core.ideas import idea_actions

from tools.adt.converter import to_plain, from_plain

from web.handler import Handler


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

