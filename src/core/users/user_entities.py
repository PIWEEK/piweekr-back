from tools.adt.types import ADTID, Field, StrField, IntField

from skame.schemas import types as t, strings as s, numeric as n, base as b
from skame.exceptions import SchemaError
from tools import validator as v


class UserForRegister(ADTID):
    user_name = StrField()
    clear_password = StrField()
    full_name = StrField()
    email = StrField()


class UserForRegisterValidator(v.Validator):
    schema = b.schema({
        "user_name": b.And(
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


class User(ADTID):
    user_name = StrField()
    password = StrField()
    full_name = StrField()
    email = StrField()
    avatar = Field(type=dict) # Format: {<section>: <icon>} where section = "head"|"body"|"legs"|"background" and value is [1-10], background must be a valid html color

