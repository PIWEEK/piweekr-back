from anillo.http import responses
from itsdangerous import JSONWebSignatureSerializer

from core.users import user_actions
from core.users import user_entities

from tools.adt.converter import to_plain, from_plain

from web.decorators import login_required
from web.handler import Handler

import settings


#######################################
## Auth
#######################################

class Login(Handler):
    def post(self, request):
        username = request.body.get("username", "")
        password = request.body.get("password", "")
        user = user_actions.get_by_username_and_password(username, password)
        if not user:
            return responses.BadRequest({"error": "Invalid username or password"})
        else:
            token_data = {"user_id": user.id}
            serializer = JSONWebSignatureSerializer(settings.SECRET_KEY)
            token = serializer.dumps(token_data).decode("ascii")

            result = to_plain(user, ignore_fields=["id", "password"])
            result["token"] = token
            return responses.Ok(result)


class Logout(Handler):
    def post(self, request):
        # TODO: add some mechanism to invalidate the token when logged out
        return responses.Ok()


#######################################
## Users
#######################################

class UsersList(Handler):
    def get(self, request):
        users = user_actions.list_users()
        return responses.Ok([
            to_plain(user, ignore_fields=["id", "password"])
            for user in users
        ])


class UserDetail(Handler):
    def get(self, request, username):
        user = user_actions.get_by_username(username)
        if not user:
            return responses.NotFound()

        return responses.Ok(to_plain(user, ignore_fields=["id", "password"]))

    @login_required
    def patch(self, request, username):
        user = user_actions.get_by_username(username)
        if not user:
            return responses.NotFound()

        if request.user.username != user.username:
            return responses.Forbidden({"error": "You can only update your user"})

        validator = user_entities.UserForUpdateValidator(request.body)
        if validator.is_valid():
            user = user_actions.update_user(
                user,
                user_entities.UserForUpdate(**validator.cleaned_data)
            )

            token_data = {"user_id": user.id}
            serializer = JSONWebSignatureSerializer(settings.SECRET_KEY)
            token = serializer.dumps(token_data).decode("ascii")

            result = to_plain(user, ignore_fields=["id", "password"])
            result["token"] = token
            return responses.Ok(result)
        else:
            return responses.BadRequest(validator.errors)

    def delete(self, request, username):
        raise NotImplementedError("TODO")
