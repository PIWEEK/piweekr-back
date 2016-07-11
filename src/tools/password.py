'''
Abstraction of i18n services with gettext.
'''

from passlib.hash import pbkdf2_sha256


def generate_hash(password):
    return pbkdf2_sha256.encrypt(password)


def verify_hash(password, password_hash):
    return pbkdf2_sha256.verify(password, password_hash)
