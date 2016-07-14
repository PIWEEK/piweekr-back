from tools.adt.types import ADTID, Field, StrField, IntField

from skame.schemas import types as t, strings as s, numeric as n, base as b
from skame.exceptions import SchemaError
from tools import validator as v


class UserForRegister(ADTID):
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


class UserForUpdate(ADTID):
    username = StrField(null=True)
    clear_password = StrField(null=True)
    full_name = StrField(null=True)
    email = StrField(null=True)
    avatar = Field(type=dict, null=True) # Format: {<section>: <icon>} where section = "head"|"body"|"legs"|"background" and value is [1-10], background must be a valid html color


class UserForUpdateValidator(v.Validator):
    schema = b.schema({
        b.Optional("username"): t.String(),
        b.Optional("clear_password"): t.String(),
        b.Optional("full_name"): t.String(),
        b.Optional("email"): b.And(
            t.String(),
            s.Email(),
        ),
        b.Optional("avatar"): t.Dict() #TODO: Improve this validation
    })

class User(ADTID):
    username = StrField()
    password = StrField()
    full_name = StrField()
    email = StrField()
    avatar = Field(type=dict) # Format: {<section>: <icon>} where section = "head"|"body"|"legs"|"background" and value is [1-10], background must be a valid html color

    def edit(self, data):
        if data.get("username", None):
            self.username = data["username"]
        if data.get("password", None):
            self.password = data["password"]
        if data.get("full_name", None):
            self.full_name = data["full_name"]
        if data.get("email", None):
            self.email = data["email"]
        if data.get("avatar", None):
            self.avatar = data["avatar"]
