from sqlalchemy.sql import select, outerjoin
from tools.adt.adt_sql import SQLADTRepository

from core.users import user_entities


repo = SQLADTRepository({
    "DB_NAME": "piweekr",
    "ECHO": False,
})

repo.add_adt_table(user_entities.User, "users")
repo.create_all_tables()


def create_user(user):
    with repo.context() as context:
        user = repo.insert_adt(context, repo.users, user)

    return user


def list_users():
    with repo.context() as context:
        users = repo.retrieve_adts(context,
            user_entities.User,
            select([repo.users])
                .order_by("full_name")
        )

    return users

