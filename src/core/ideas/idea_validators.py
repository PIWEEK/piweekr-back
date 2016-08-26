# -*- coding: utf-8 -*-

from skame.schemas import types as t, strings as s, numeric as n, base as b
from skame.exceptions import SchemaError
from tools import validator as v


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
        b.Optional("invited_usernames"): t.List(),
    })


class IdeaForUpdateValidator(v.Validator):
    schema = b.schema({
        b.Optional("title"): b.And(
            t.String(),
            s.NotEmpty(),
        ),
        b.Optional("description"): b.And(
            t.String(),
            s.NotEmpty(),
        ),
        b.Optional("is_public"): t.Bool(),
    })


class IdeaAddInvitedValidator(v.Validator):
    schema = b.schema({
        "invited_usernames": t.List(),
    })


class IdeaRemoveInvitedValidator(v.Validator):
    schema = b.schema({
        "invited_username": b.And(
            t.String(),
            s.NotEmpty(),
        ),
    })


class IdeaCommentForCreateValidator(v.Validator):
    schema = b.schema({
        "content": b.And(
            t.String(),
            s.NotEmpty(),
        )
    })


class IdeaReactionForCreateValidator(v.Validator):
    schema = b.schema({
        "code": b.And(
            t.String(),
            s.NotEmpty(),
        )
    })

