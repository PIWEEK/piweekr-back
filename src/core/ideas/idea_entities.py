# -*- coding: utf-8 -*-

from tools.adt.types import ADTID, Field, StrField, IntField, BoolField, ArrowDateTimeField
from tools.adt.relationships import Relationship1N, RoleSingle, RoleMulti


class IdeaForCreate(ADTID):
    title = StrField()
    description = StrField()
    is_public = BoolField()


class Idea(ADTID):
    uuid = StrField()
    title = StrField()
    description = StrField()
    owner_id = IntField()
    created_at = ArrowDateTimeField()
    is_public = BoolField()
    forked_from = IntField(null=True)
    comments_count = IntField()
    reactions_counts = Field(type=dict) # Format: {<emoji>: <counter>}


from core.users import user_entities

class IdeaHasOwner(Relationship1N):
    role_1 = RoleSingle(role_class=user_entities.User, role_name="owner")
    role_n = RoleMulti(role_class=Idea, role_name="ideas", role_fk="owner_id", required=True)

