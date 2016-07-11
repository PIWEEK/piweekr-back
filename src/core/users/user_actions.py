from tools.password import generate_hash, verify_hash
from services.repository.sql.users import user_repository

from . import user_entities


def register_new_user(user_for_register):
    user = user_entities.User(
        user_name = user_for_register.user_name,
        password = generate_hash(user_for_register.clear_password),
        full_name = user_for_register.full_name,
        email = user_for_register.email,
        avatar = ''
    )

    return user_repository.create_user(user)


def list_users():
    users = user_repository.list_users()
    return users

