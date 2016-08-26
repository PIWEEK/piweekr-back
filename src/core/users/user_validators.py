# -*- coding: utf-8 -*-

from skame.schemas import types as t, strings as s, numeric as n, base as b
from skame.exceptions import SchemaError
from tools import validator as v


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

