from sqlalchemy.sql import select, outerjoin
from tools.adt.adt_sql import SQLADTRepository

from core import entities


repo = SQLADTRepository({
    "DB_NAME": "piweekr",
    "ECHO": False,
})

repo.add_adt_table(entities.User, "users")
repo.create_all_tables()


def create_user(user):
    with repo.context() as context:
        user = repo.insert_adt(context, repo.users, user)

    return user

