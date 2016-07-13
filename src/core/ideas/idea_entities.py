# -*- coding: utf-8 -*-

from tools.adt.types import ADTID, Field, StrField, IntField, BoolField, ArrowDateTimeField
from tools.adt.relationships import Relationship1N, RoleSingle, RoleMulti

from skame.schemas import types as t, strings as s, numeric as n, base as b
from skame.exceptions import SchemaError
from tools import validator as v

from core.users import user_entities


class IdeaForCreate(ADTID):
    title = StrField()
    description = StrField()
    is_public = BoolField()


class IdeaForCreateValidator(v.Validator):
    schema = b.schema({
        "title": b.And(
            t.String(),
            s.NotEmpty(),
        ),
        "description": b.And(
            t.String(),
            s.NotEmpty(),
        ),
        "is_public": t.Bool(),
    })


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


class IdeaHasOwner(Relationship1N):
    role_1 = RoleSingle(role_class=user_entities.User, role_name="owner")
    role_n = RoleMulti(role_class=Idea, role_name="ideas", role_fk="owner_id", required=True)


class IdeaInvited(ADTID):
    idea_id = IntField()
    user_id = IntField()


class IdeaInvitedHasIdea(Relationship1N):
    role_1 = RoleSingle(role_class=Idea, role_name="idea")
    role_n = RoleMulti(role_class=IdeaInvited, role_name="ideas_invited", role_fk="idea_id", required=True)


class IdeaInvitedHasUser(Relationship1N):
    role_1 = RoleSingle(role_class=user_entities.User, role_name="user")
    role_n = RoleMulti(role_class=IdeaInvited, role_name="ideas_invited", role_fk="user_id", required=True)

