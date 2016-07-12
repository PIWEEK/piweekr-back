# -*- coding: utf-8 -*-

from tools.adt.types import ADTID, Field, StrField, IntField, ArrowDateTimeField


class Project(ADTID):
    uuid = StrField()
    title = StrField()
    description = StrField()
    technologies = Field(type=list)
    needs = StrField()
    logo = StrField()
    piweek_id = IntField()
    idea_from_id = IntField(null=True)
    owner_id = IntField()
    created_at = ArrowDateTimeField()
