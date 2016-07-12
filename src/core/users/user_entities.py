from tools.adt.types import ADTID, StrField, IntField


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
    avatar = StrField(null=True)

