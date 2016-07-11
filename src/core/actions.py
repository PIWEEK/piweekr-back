from tools.password import generate_hash, verify_hash
from services.repository import sql

from . import entities


def register_new_user(user_for_register):
    user = entities.User(
        user_name = user_for_register.user_name,
        password = generate_hash(user_for_register.clear_password),
        full_name = user_for_register.full_name,
        email = user_for_register.email,
        description = ''
    )

    return sql.create_user(user)

