from tools.adt.types import ADTID, StrField, IntField, BoolField, DateTimeField


class Idea(ADTID):
    uuid = StrField()
    title = StrField()
    description = StrField()
    owner_id = IntField()
    created_at = DateTimeField()
    is_public = BoolField()
    forked_from = IntField(null=True)

