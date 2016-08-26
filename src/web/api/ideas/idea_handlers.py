from copy import deepcopy
from anillo.http import responses

from core.ideas import idea_entities, idea_validators, idea_actions
from core.users import user_entities, user_actions

from tools.adt.converter import to_plain, from_plain

from web.handler import Handler
from web.decorators import login_required

from web.api.loaders_and_checkers import *
from web.api import exceptions


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
        validator = idea_validators.IdeaForCreateValidator(request.body)
        if validator.is_valid():
            if validator.cleaned_data["is_public"] and validator.cleaned_data.get("invited_usernames"):
                raise exceptions.BadRequest("Only private ideas can have invited users")

            invited_users = []
            for invited_username in validator.cleaned_data["invited_usernames"]:
                invited_user = load_user_secondary(invited_username)
                check_user_is_not_self(request.user, invited_user)
                invited_users.append(invited_user)

            data = deepcopy(validator.cleaned_data)
            del data["invited_usernames"]
            data["invited_users"] = invited_users

            idea = idea_actions.create_idea(
                request.user,
                idea_entities.IdeaForCreate(**data)
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
        idea = load_idea(idea_uuid)
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
        idea = load_idea(idea_uuid)
        check_user_is_owner_of_idea(request.user, idea)

        validator = idea_validators.IdeaForUpdateValidator(request.body)
        if validator.is_valid():
            idea = idea_actions.update_idea(
                request.user,
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
        idea = load_idea(idea_uuid)
        check_user_is_not_owner_of_idea(request.user, idea)

        forked_idea = idea_actions.fork_idea(request.user, idea)

        return responses.Ok(to_plain(forked_idea, ignore_fields=["id", "is_active"]))


class IdeaPromote(Handler):
    def post(self, request, idea_uuid):
        idea = load_idea(idea_uuid)
        check_user_is_owner_of_idea(request.user, idea)

        project = idea_actions.promote_idea(request.user, idea)

        return responses.Ok(to_plain(project, ignore_fields=["id"]))


#######################################
## Invited
#######################################

class IdeaInvitedList(Handler):
    def get(self, request, idea_uuid):
        idea = load_idea(idea_uuid)

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
        idea = load_idea(idea_uuid)
        check_user_is_owner_of_idea(request.user, idea)
        check_idea_is_private(idea)

        validator = idea_validators.IdeaAddInvitedValidator(request.body)
        if validator.is_valid():

            invited_users = []
            for invited_username in validator.cleaned_data["invited_usernames"]:
                invited_user = load_user_secondary(invited_username)
                check_user_is_not_self(request.user, invited_user)
                check_user_is_not_invited_to_idea(invited_user, idea)
                invited_users.append(invited_user)

            idea_actions.invite_users(request.user, idea, invited_users)

            return responses.Ok()
        else:
            return responses.BadRequest(validator.errors)

    @login_required
    def delete(self, request, idea_uuid):
        idea = load_idea(idea_uuid)
        check_user_is_owner_of_idea(request.user, idea)
        check_idea_is_private(idea)

        validator = idea_validators.IdeaRemoveInvitedValidator(request.body)
        if validator.is_valid():

            invited_username = validator.cleaned_data["invited_username"]

            invited_user = load_user_secondary(invited_username)
            check_user_is_not_self(request.user, invited_user)
            invited = load_user_invited_to_idea(invited_user, idea)

            idea_actions.remove_invited_user(request.user, idea, invited)

            return responses.Ok()
        else:
            return responses.BadRequest(validator.errors)


#######################################
## Comment
#######################################

class IdeaCommentsList(Handler):
    def get(self, request, idea_uuid):
        idea = load_idea(idea_uuid)

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
        idea = load_idea(idea_uuid)

        validator = idea_validators.IdeaCommentForCreateValidator(request.body)
        if validator.is_valid():
            if not idea.is_public and idea.owner_id != request.user.id:
                check_user_is_invited_to_idea(request.user, idea)

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
        idea = load_idea(idea_uuid)

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
        idea = load_idea(idea_uuid)

        validator = idea_validators.IdeaReactionForCreateValidator(request.body)
        if validator.is_valid():
            if not idea.is_public and idea.owner_id != request.user.id:
                check_user_is_invited_to_idea(request.user, idea)

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
