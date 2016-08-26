# -*- coding: utf-8 -*-

from skame.schemas import types as t, strings as s, numeric as n, base as b
from skame.exceptions import SchemaError
from tools import validator as v


class ProjectCommentForCreateValidator(v.Validator):
    schema = b.schema({
        "content": b.And(
            t.String(),
            s.NotEmpty(),
        )
    })


class ProjectReactionForCreateValidator(v.Validator):
    schema = b.schema({
        "code": b.And(
            t.String(),
            s.NotEmpty(),
        )
    })

