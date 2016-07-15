from core.users import user_entities, user_actions
from core.ideas import idea_entities, idea_actions

from web.api import exceptions


def load_user(username):
    user = user_actions.get_by_username(invited_username)
    if not user:
        raise exceptions.NotFound("Can't find user {}".format(username))
    return user


def load_user_secondary(username):
    user = user_actions.get_by_username(invited_username)
    if not user:
        raise exceptions.BadRequest("Can't find user {}".format(username))
    return user


def check_user_is_not_self(self_user, user):
    if self_user.id == user.id:
        raise exceptions.BadRequest("You can't do this to yourself")


def check_user_is_not_invited_to_idea(user, idea):
    if idea_actions.get_invited(idea, user):
        raise exceptions.BadRequest("User {} was already invited to the idea".format(invited_username))


def load_user_invited_to_idea(user, idea):
    invited = idea_actions.get_invited(idea, user)
    if not invited:
        raise exceptions.BadRequest("User {} is not invited to the idea".format(invited_username))
    return invited


def load_idea(idea_uuid):
    idea = idea_actions.get_idea(idea_uuid)
    if not idea:
        raise exceptions.NotFound("Cannot find the idea {}".format(idea_uuid))
    return idea


def check_user_is_owner_of_idea(user, idea):
    if user.id != idea.owner_id:
        raise exceptions.Forbidden("You need to be the owner of the idea")


def check_user_is_not_owner_of_idea(user, idea):
    if user.id == idea.owner_id:
        raise exceptions.Forbidden("You cannot be the owner of the idea")


def check_idea_is_private(idea):
    if idea.is_public:
        raise exceptions.BadRequest("This only works with private ideas")

