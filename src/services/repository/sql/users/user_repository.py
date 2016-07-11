from sqlalchemy.sql import select, outerjoin
from tools.adt.adt_sql import SQLADTRepository

from core.users import user_entities

import settings

repo = SQLADTRepository(settings.DB_OPTIONS)

repo.add_adt_table(user_entities.User, "users")
repo.create_all_tables()


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

