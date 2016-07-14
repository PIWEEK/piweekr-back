# -*- coding: utf-8 -*-

from tools.adt.types import ADTID, Field, StrField, IntField, ArrowDateTimeField
from tools.adt.relationships import Relationship1N, RoleSingle, RoleMulti

from skame.schemas import types as t, strings as s, numeric as n, base as b
from skame.exceptions import SchemaError
from tools import validator as v


#######################################
## Project
#######################################

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
    comments_count = IntField()
    reactions_counts = Field(type=dict) # Format: {<emoji>: <counter>}


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

class ProjectInterested(ADTID):
    project_id = IntField()
    user_id = IntField()


class ProjectInterestedHasProject(Relationship1N):
    role_1 = RoleSingle(role_class=Project, role_name="project")
    role_n = RoleMulti(role_class=ProjectInterested, role_name="projects_interested", role_fk="project_id", required=True)


class ProjectInterestedHasUser(Relationship1N):
    role_1 = RoleSingle(role_class=user_entities.User, role_name="user")
    role_n = RoleMulti(role_class=ProjectInterested, role_name="projects_interested", role_fk="user_id", required=True)


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

class ProjectCommentForCreate(ADTID):
    content = StrField()


class ProjectCommentForCreateValidator(v.Validator):
    schema = b.schema({
        "content": b.And(
            t.String(),
            s.NotEmpty(),
        )
    })


class ProjectComment(ADTID):
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

