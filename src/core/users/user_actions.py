# -*- coding: utf-8 -*-

from copy import deepcopy

from tools.password import generate_hash, verify_hash
from services.repository.sql.users import user_repository

from . import user_entities


def register_new_user(user_for_register):
    user = user_entities.User(
        username = user_for_register.username,
        password = generate_hash(user_for_register.clear_password),
        full_name = user_for_register.full_name,
        email = user_for_register.email,
        avatar = {
            "head": 1,
            "body": 1,
            "legs": 1,
            "background": "#fabada"
        }
    )
    return user_repository.create(user)


def get_by_id(user_id):
    return user_repository.retrieve_by_id(user_id)


def get_by_username(username):
    return user_repository.retrieve_by_username(username)


def get_by_username_and_password(username, clear_password):
    user = user_repository.retrieve_by_username(username)
    if user:
        if not verify_hash(clear_password, user.password):
            user = None
    return user


def list_users():
    users = user_repository.list()
    return users


def update_user(user, updates):
    data = deepcopy(updates.to_dict())
    if data.get("clear_password", None):
        data["password"] = generate_hash(data["clear_password"])
        del data["clear_password"]
    user.edit(data)

    return user_repository.update(user)
