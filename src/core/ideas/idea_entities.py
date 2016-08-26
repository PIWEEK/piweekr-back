# -*- coding: utf-8 -*-

from tools.adt.types import ADT, ADT_WITH_ID, Field, StrField, IntField, BoolField, ArrowDateTimeField
from tools.adt.relationships import Relationship1N, RoleSingle, RoleMulti

from skame.schemas import types as t, strings as s, numeric as n, base as b
from skame.exceptions import SchemaError
from tools import validator as v

from core.users import user_entities


#######################################
## Idea
#######################################

class IdeaForCreate(ADT):
    title = StrField()
    description = StrField()
    is_public = BoolField()
    invited_users = Field(type=list, null=True) # List of users


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


class IdeaForUpdate(ADT):
    title = StrField(null=True)
    description = StrField(null=True)
    is_public = BoolField(null=True)


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


class Idea(ADT_WITH_ID):
    uuid = StrField()
    is_active = BoolField()
    title = StrField()
    description = StrField()
    owner_id = IntField()
    created_at = ArrowDateTimeField()
    is_public = BoolField()
    forked_from_id = IntField(null=True)
    comments_count = IntField()
    reactions_counts = Field(type=dict) # Format: {<emoji>: <counter>}

    def edit(self, idea_for_update):
        if idea_for_update.title != None:
            self.title = idea_for_update.title
        if idea_for_update.description != None:
            self.description = idea_for_update.description
        if idea_for_update.is_public != None:
            self.is_public = idea_for_update.is_public

    def deactivate(self):
        self.is_active = False

    def activate(self):
        self.is_active = True

    def increase_comment_count(self):
        self.comments_count += 1

    def decrease_comment_count(self):
        """
        pre:
            self.comments_count > 0"
        """
        self.comments_count -= 1

    def increase_reaction_count(self, code):
        if not code in self.reactions_counts:
            self.reactions_counts[code] = 0
        self.reactions_counts[code] += 1

    def decrease_reaction_count(self, code):
        """
        pre:
            code in self.reactions_counts
            self.reactions_counts[code] > 0
        """
        self.reactions_counts[code] -= 1
        if self.reactions_counts[code] <= 0:
            del self.reactions_counts[code]


class IdeaHasOwner(Relationship1N):
    role_1 = RoleSingle(role_class=user_entities.User, role_name="owner")
    role_n = RoleMulti(role_class=Idea, role_name="ideas", role_fk="owner_id", required=True)


class IdeaHasForks(Relationship1N):
    role_1 = RoleSingle(role_class=Idea, role_name="forked_from")
    role_n = RoleMulti(role_class=Idea, role_name="forks", role_fk="forked_from_id", required=False)


#######################################
## Inviteds
#######################################

class IdeaInvited(ADT_WITH_ID):
    idea_id = IntField()
    user_id = IntField()


class IdeaInvitedHasIdea(Relationship1N):
    role_1 = RoleSingle(role_class=Idea, role_name="idea")
    role_n = RoleMulti(role_class=IdeaInvited, role_name="users_invited", role_fk="idea_id", required=True)


class IdeaInvitedHasUser(Relationship1N):
    role_1 = RoleSingle(role_class=user_entities.User, role_name="user")
    role_n = RoleMulti(role_class=IdeaInvited, role_name="ideas_invited", role_fk="user_id", required=True)


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


#######################################
## Comment
#######################################

class IdeaCommentForCreate(ADT_WITH_ID):
    content = StrField()


class IdeaCommentForCreateValidator(v.Validator):
    schema = b.schema({
        "content": b.And(
            t.String(),
            s.NotEmpty(),
        )
    })


class IdeaComment(ADT_WITH_ID):
    uuid = StrField()
    content = StrField()
    owner_id = IntField()
    idea_id = IntField()
    created_at = ArrowDateTimeField()


class IdeaCommentHasOwner(Relationship1N):
    role_1 = RoleSingle(role_class=user_entities.User, role_name="owner")
    role_n = RoleMulti(role_class=IdeaComment, role_name="idea_comments", role_fk="owner_id", required=True)


class IdeaCommentFromIdea(Relationship1N):
    role_1 = RoleSingle(role_class=Idea, role_name="idea")
    role_n = RoleMulti(role_class=IdeaComment, role_name="comments", role_fk="idea_id", required=True)


#######################################
## Reaction
#######################################

class IdeaReactionForCreate(ADT_WITH_ID):
    code = StrField()


class IdeaReactionForCreateValidator(v.Validator):
    schema = b.schema({
        "code": b.And(
            t.String(),
            s.NotEmpty(),
        )
    })


class IdeaReaction(ADT_WITH_ID):
    uuid = StrField()
    code = StrField()
    owner_id = IntField()
    idea_id = IntField()
    created_at = ArrowDateTimeField()


class IdeaReactionHasOwner(Relationship1N):
    role_1 = RoleSingle(role_class=user_entities.User, role_name="owner")
    role_n = RoleMulti(role_class=IdeaReaction, role_name="idea_reactions", role_fk="owner_id", required=True)


class IdeaReactionFromIdea(Relationship1N):
    role_1 = RoleSingle(role_class=Idea, role_name="idea")
    role_n = RoleMulti(role_class=IdeaReaction, role_name="reactions", role_fk="idea_id", required=True)

