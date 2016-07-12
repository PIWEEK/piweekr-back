from sqlalchemy import Column
from sqlalchemy.sql import select, outerjoin
from sqlalchemy.dialects.postgresql import JSONB

from tools.adt.adt_sql import SQLADTRepository

from core.users import user_entities

from services.repository.sql import repo

repo.add_adt_table(user_entities.User, "users",
    manual_columns={
        "avatar": Column('avatar', JSONB),
    }
)


def create(user):
    with repo.context() as context:
        user = repo.insert_adt(context, repo.users, user)
    return user


def list():
    with repo.context() as context:
        users = repo.retrieve_adts(context,
            user_entities.User,
            select([repo.users])
                .order_by("full_name")
        )
    return users


def retrieve_by_user_name(user_name):
    with repo.context() as context:
        user = repo.retrieve_single_adt(context,
            user_entities.User,
            select([repo.users])
                .where(repo.users.c.user_name == user_name)
        )
    return user

