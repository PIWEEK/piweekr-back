from core.users import user_entities, user_actions
from core.ideas import idea_entities, idea_actions

from web.api import exceptions


#######################################
## Users
#######################################

def load_user(username):
    user = user_actions.get_by_username(username)
    if not user:
        raise exceptions.NotFound("Can't find user {}".format(username))
    return user


def load_user_secondary(username):
    user = user_actions.get_by_username(username)
    if not user:
        raise exceptions.BadRequest("Can't find user {}".format(username))
    return user


def check_user_is_self(self_user, user):
    if self_user.id != user.id:
        raise exceptions.BadRequest("You can only do this to yourself")


def check_user_is_not_self(self_user, user):
    if self_user.id == user.id:
        raise exceptions.BadRequest("You can't do this to yourself")


#######################################
## Ideas
#######################################


def load_idea(idea_uuid):
    idea = idea_actions.get_idea(idea_uuid)
    if not idea:
        raise exceptions.NotFound("Cannot find the idea {}".format(idea_uuid))
    return idea


def check_idea_is_private(idea):
    if idea.is_public:
        raise exceptions.BadRequest("This only works with private ideas")


def check_user_is_owner_of_idea(user, idea):
    if user.id != idea.owner_id:
        raise exceptions.Forbidden("You need to be the owner of the idea")


def check_user_is_not_owner_of_idea(user, idea):
    if user.id == idea.owner_id:
        raise exceptions.Forbidden("You cannot be the owner of the idea")


def check_user_is_invited_to_idea(user, idea):
    if not idea_actions.get_invited(idea, user):
        raise exceptions.BadRequest("User {} is not invited to the idea".format(user.username))


def check_user_is_not_invited_to_idea(user, idea):
    if idea_actions.get_invited(idea, user):
        raise exceptions.BadRequest("User {} was already invited to the idea".format(user.username))


def load_user_invited_to_idea(user, idea):
    invited = idea_actions.get_invited(idea, user)
    if not invited:
        raise exceptions.BadRequest("User {} is not invited to the idea".format(user.username))
    return invited


#######################################
## Projects
#######################################


def load_project(project_uuid):
    project = project_actions.get_project(project_uuid)
    if not project:
        raise exceptions.NotFound("Cannot find the project {}".format(project_uuid))
    return project


def check_user_is_owner_of_project(user, project):
    if user.id != project.owner_id:
        raise exceptions.Forbidden("You need to be the owner of the project")


def check_user_is_not_owner_of_project(user, project):
    if user.id == project.owner_id:
        raise exceptions.Forbidden("You cannot be the owner of the project")


def check_user_is_interested_in_project(user, project):
    if not project_actions.get_interested(project, user):
        raise exceptions.BadRequest("User {} is not interested in the project".format(user.username))


def check_user_is_not_interested_in_project(user, project):
    if project_actions.get_interested(project, user):
        raise exceptions.BadRequest("User {} was already interested in the project".format(user.username))


def check_user_is_participant_in_project(user, project):
    if not project_actions.get_participant(project, user):
        raise exceptions.BadRequest("User {} is not participant in the project".format(user.username))


def check_user_is_not_participant_in_project(user, project):
    if project_actions.get_participant(project, user):
        raise exceptions.BadRequest("User {} was already participant in the project".format(user.username))

