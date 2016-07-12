from tools.adt.types import ADTID, Field, StrField, IntField


class UserForRegister(ADTID):
    user_name = StrField()
    clear_password = StrField()
    full_name = StrField()
    email = StrField()


class User(ADTID):
    user_name = StrField()
    password = StrField()
    full_name = StrField()
    email = StrField()
    avatar = Field(type=dict) # Format: {<section>: <icon>} where section = "head"|"body"|"legs" and value is [1-10]

