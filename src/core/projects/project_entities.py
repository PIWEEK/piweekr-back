# -*- coding: utf-8 -*-

from tools.adt.types import ADT_WITH_ID, Field, StrField, IntField, ArrowDateTimeField
from tools.adt.relationships import Relationship1N, RoleSingle, RoleMulti

from skame.schemas import types as t, strings as s, numeric as n, base as b
from skame.exceptions import SchemaError
from tools import validator as v


#######################################
## Project
#######################################

class Project(ADT_WITH_ID):
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
    comments_count = IntField()
    reactions_counts = Field(type=dict) # Format: {<emoji>: <counter>}

    def increase_comment_count(self):
        self.comments_count += 1

    def decrease_comment_count(self):
        if self.comments_count > 0:
            self.comments_count -= 1

    def increase_reaction_count(self, code):
        if not code in self.reactions_counts:
            self.reactions_counts[code] = 0
        self.reactions_counts[code] += 1

    def decrease_reaction_count(self, code):
        if code in self.reactions_counts:
            self.reactions_counts[code] -= 1
            if self.reactions_counts[code] <= 0:
                del self.reactions_counts[code]


from core.users import user_entities

class ProjectHasOwner(Relationship1N):
    role_1 = RoleSingle(role_class=user_entities.User, role_name="owner")
    role_n = RoleMulti(role_class=Project, role_name="owners", role_fk="owner_id", required=True)


from core.ideas import idea_entities

class ProjectIsFromIdea(Relationship1N):
    role_1 = RoleSingle(role_class=idea_entities.Idea, role_name="idea_from")
    role_n = RoleMulti(role_class=Project, role_name="projects", role_fk="idea_from_id", required=True)


#######################################
## Interested
#######################################

class ProjectInterested(ADT_WITH_ID):
    project_id = IntField()
    user_id = IntField()


class ProjectInterestedHasProject(Relationship1N):
    role_1 = RoleSingle(role_class=Project, role_name="project")
    role_n = RoleMulti(role_class=ProjectInterested, role_name="users_interested", role_fk="project_id", required=True)


class ProjectInterestedHasUser(Relationship1N):
    role_1 = RoleSingle(role_class=user_entities.User, role_name="user")
    role_n = RoleMulti(role_class=ProjectInterested, role_name="projects_interested", role_fk="user_id", required=True)


#######################################
## Participants
#######################################

class ProjectParticipant(ADT_WITH_ID):
    project_id = IntField()
    user_id = IntField()


class ProjectParticipantHasProject(Relationship1N):
    role_1 = RoleSingle(role_class=Project, role_name="project")
    role_n = RoleMulti(role_class=ProjectParticipant, role_name="users_participant", role_fk="project_id", required=True)


class ProjectParticipantHasUser(Relationship1N):
    role_1 = RoleSingle(role_class=user_entities.User, role_name="user")
    role_n = RoleMulti(role_class=ProjectParticipant, role_name="projects_participant", role_fk="user_id", required=True)


#######################################
## Piweek
#######################################


# TODO:
#from core.piweeks import piweek_entities
#
#class ProjectIsFromPiweek(Relationship11):
#    role_from = RoleSingle(role_class=piweek_entities.Piweek, role_name="piweek")
#    role_to = RoleDingle(role_class=Project, role_name="project", role_fk="piweek_id", required=True)


#######################################
## Comment
#######################################

class ProjectCommentForCreate(ADT_WITH_ID):
    content = StrField()


class ProjectCommentForCreateValidator(v.Validator):
    schema = b.schema({
        "content": b.And(
            t.String(),
            s.NotEmpty(),
        )
    })


class ProjectComment(ADT_WITH_ID):
    uuid = StrField()
    content = StrField()
    owner_id = IntField()
    project_id = IntField()
    created_at = ArrowDateTimeField()


class ProjectCommentHasOwner(Relationship1N):
    role_1 = RoleSingle(role_class=user_entities.User, role_name="owner")
    role_n = RoleMulti(role_class=ProjectComment, role_name="project_comments", role_fk="owner_id", required=True)


class ProjectCommentFromProject(Relationship1N):
    role_1 = RoleSingle(role_class=Project, role_name="project")
    role_n = RoleMulti(role_class=ProjectComment, role_name="comments", role_fk="project_id", required=True)


#######################################
## Reaction
#######################################

class ProjectReactionForCreate(ADT_WITH_ID):
    code = StrField()


class ProjectReactionForCreateValidator(v.Validator):
    schema = b.schema({
        "code": b.And(
            t.String(),
            s.NotEmpty(),
        )
    })


class ProjectReaction(ADT_WITH_ID):
    uuid = StrField()
    code = StrField()
    owner_id = IntField()
    project_id = IntField()
    created_at = ArrowDateTimeField()


class ProjectReactionHasOwner(Relationship1N):
    role_1 = RoleSingle(role_class=user_entities.User, role_name="owner")
    role_n = RoleMulti(role_class=ProjectReaction, role_name="project_reactions", role_fk="owner_id", required=True)


class ProjectReactionFromProject(Relationship1N):
    role_1 = RoleSingle(role_class=Project, role_name="project")
    role_n = RoleMulti(role_class=ProjectReaction, role_name="reactions", role_fk="project_id", required=True)

