from tools.password import generate_hash, verify_hash
from services.repository.sql.ideas import idea_repository

from . import idea_entities


def list_ideas():
    ideas = idea_repository.list()
    return ideas

