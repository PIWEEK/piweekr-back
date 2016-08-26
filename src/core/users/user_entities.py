from tools.adt.types import ADT, ADT_WITH_ID, Field, StrField, IntField

from skame.schemas import types as t, strings as s, numeric as n, base as b
from skame.exceptions import SchemaError
from tools import validator as v


#######################################
## User
#######################################


class UserForRegister(ADT):
    username = StrField()
    clear_password = StrField()
    full_name = StrField()
    email = StrField()


class UserForRegisterValidator(v.Validator):
    schema = b.schema({
        "username": b.And(
            t.String(),
            s.NotEmpty(),
        ),
        "clear_password": b.And(
            t.String(),
            s.NotEmpty(),
        ),
        "full_name": b.And(
            t.String(),
            s.NotEmpty(),
        ),
        "email": b.And(
            t.String(),
            s.NotEmpty(),
            s.Email(),
        ),
    })


class UserForUpdate(ADT):
    username = StrField(null=True)
    clear_password = StrField(null=True)
    password = StrField(null=True)
    full_name = StrField(null=True)
    email = StrField(null=True)
    avatar = Field(type=dict, null=True) # See avatar in User

    def set_password(self, password):
        """
        pre:
            password == None or len(password) > 0
        """
        self.password = password


class UserForUpdateValidator(v.Validator):
    schema = b.schema({
        b.Optional("username"): b.And(
            t.String(),
            s.NotEmpty(),
        ),
        b.Optional("clear_password"): b.And(
            t.String(),
            s.NotEmpty(),
        ),
        b.Optional("full_name"): b.And(
            t.String(),
            s.NotEmpty(),
        ),
        b.Optional("email"): b.And(
            t.String(),
            s.NotEmpty(),
            s.Email(),
        ),
        b.Optional("avatar"): t.Dict() #TODO: Improve this validation
    })


class User(ADT_WITH_ID):
    username = StrField()
    password = StrField()
    full_name = StrField()
    email = StrField()
    avatar = Field(type=dict) # Format: {<section>: <icon>} where section = "head"|"body"|"legs"|"background"
                              # and value is [1-10], background must be a valid html color

    def edit(self, user_for_update):
        if user_for_update.username != None:
            self.username = user_for_update.username
        if user_for_update.password != None:
            self.password = user_for_update.password
        if user_for_update.full_name != None:
            self.full_name = user_for_update.full_name
        if user_for_update.email != None:
            self.email = user_for_update.email
        if user_for_update.avatar != None:
            self.avatar = user_for_update.avatar

