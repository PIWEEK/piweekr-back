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
        ideas = idea_actions.list_ideas(request.user)
        return responses.Ok([
            to_plain(idea, ignore_fields=["id", "is_active"],
                relationships = {
                    "owner": {"ignore_fields": ["id", "password"]},
                    "forked_from": {
                        "only_fields": ["title"],
                        "relationships": {
                            "owner": {"ignore_fields": ["id", "password"]},
                        }
                    }
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
            return responses.Ok(to_plain(
                idea,
                ignore_fields=["id", "is_active"],
                relationships={
                    "owner": {"ignore_fields": ["id", "password"]},
                }
            ))
        else:
            return responses.BadRequest(validator.errors)


class IdeaDetail(Handler):
    def get(self, request, idea_uuid):
        idea = idea_actions.get_idea(idea_uuid)
        if not idea:
            return responses.NotFound()

        return responses.Ok(to_plain(
            idea,
            ignore_fields=["id", "is_active"],
            relationships = {
                "owner": {"ignore_fields": ["id", "password"]},
                "forked_from": {
                    "only_fields": ["title"],
                    "relationships": {
                        "owner": {"ignore_fields": ["id", "password"]},
                    }
                }
            }
        ))

    @login_required
    def patch(self, request, idea_uuid):
        idea = idea_actions.get_idea(idea_uuid)
        if not idea:
            return responses.NotFound()

        if request.user.id != idea.owner_id:
            return responses.Forbidden({"error": "You can only update your ideas"})

        validator = idea_entities.IdeaForUpdateValidator(request.body)
        if validator.is_valid():
            idea = idea_actions.update_idea(
                idea,
                idea_entities.IdeaForUpdate(**validator.cleaned_data)
            )
            return responses.Ok(to_plain(
                idea,
                ignore_fields=["id", "is_active"],
                relationships = {
                    "owner": {"ignore_fields": ["id", "password"]},
                    "forked_from": {
                        "only_fields": ["title"],
                        "relationships": {
                            "owner": {"ignore_fields": ["id", "password"]},
                        }
                    }
                }
            ))
        return responses.BadRequest(validator.errors)

    def delete(self, request):
        raise NotImplementedError("TODO")


class IdeaFork(Handler):
    def post(self, request, idea_uuid):
        idea = idea_actions.get_idea(idea_uuid)
        if not idea:
            return responses.NotFound()

        forked_idea = idea_actions.fork_idea(request.user, idea)

        return responses.Ok(to_plain(forked_idea, ignore_fields=["id", "is_active"]))


class IdeaPromote(Handler):
    def post(self, request, idea_uuid):
        idea = idea_actions.get_idea(idea_uuid)
        if not idea:
            return responses.NotFound()

        project = idea_actions.promote_idea(request.user, idea)

        return responses.Ok(to_plain(project, ignore_fields=["id"]))


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

    @login_required
    def post(self, request, idea_uuid):
        idea = idea_actions.get_idea(idea_uuid)
        if not idea:
            return responses.NotFound()

        validator = idea_entities.IdeaAddInvitedValidator(request.body)
        if validator.is_valid():
            idea_actions.invite_users(request.user, idea, validator.cleaned_data["invited_usernames"])
            return responses.Ok()
        else:
            return responses.BadRequest(validator.errors)

    @login_required
    def delete(self, request, idea_uuid):
        idea = idea_actions.get_idea(idea_uuid)
        if not idea:
            return responses.NotFound()

        validator = idea_entities.IdeaRemoveInvitedValidator(request.body)
        if validator.is_valid():
            idea_actions.remove_invited_user(request.user, idea, validator.cleaned_data["invited_username"])
            return responses.Ok()
        else:
            return responses.BadRequest(validator.errors)


#######################################
## Comment
#######################################

class IdeaCommentsList(Handler):
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
        idea = idea_actions.get_idea(idea_uuid)
        if not idea:
            return responses.NotFound()

        validator = idea_entities.IdeaCommentForCreateValidator(request.body)
        if validator.is_valid():
            comment = idea_actions.create_comment(
                request.user,
                idea,
                idea_entities.IdeaCommentForCreate(**validator.cleaned_data)
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
    def delete(self, request, idea_uuid):
        raise NotImplementedError("TODO")


#######################################
## Reaction
#######################################

class IdeaReactionsList(Handler):
    def get(self, request, idea_uuid):
        idea = idea_actions.get_idea(idea_uuid)
        if not idea:
            return responses.NotFound()

        reactions = idea_actions.list_reactions(idea)
        return responses.Ok([
            to_plain(reaction, ignore_fields=["id"],
                relationships = {
                    "owner": {"ignore_fields": ["id", "password"]},
                }
            )
            for reaction in reactions
        ])

    @login_required
    def post(self, request, idea_uuid):
        idea = idea_actions.get_idea(idea_uuid)
        if not idea:
            return responses.NotFound()

        validator = idea_entities.IdeaReactionForCreateValidator(request.body)
        if validator.is_valid():
            reaction = idea_actions.create_reaction(
                request.user,
                idea,
                idea_entities.IdeaReactionForCreate(**validator.cleaned_data)
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
    def delete(self, request, idea_uuid):
        raise NotImplementedError("TODO")
