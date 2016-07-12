# -*- coding: utf-8 -*-

from tools.adt.types import ADTID, StrField, IntField, BoolField, ArrowDateTimeField


class Idea(ADTID):
    uuid = StrField()
    title = StrField()
    description = StrField()
    owner_id = IntField()
    created_at = ArrowDateTimeField()
    is_public = BoolField()
    forked_from = IntField(null=True)
