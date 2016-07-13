# -*- coding: utf-8 -*-

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
    if updates.username:
        user.update_username(updates.username)
    if updates.clear_password:
        user.update_password(generate_hash(updates.clear_password))
    if updates.full_name:
        user.update_full_name(updates.full_name)
    if updates.email:
        user.update_email(updates.email)
    if updates.avatar:
        user.update_avatar(updates.avatar)

    return user_repository.update(user)
