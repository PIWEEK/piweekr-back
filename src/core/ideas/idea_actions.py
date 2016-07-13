from tools.password import generate_hash, verify_hash
from services.repository.sql.ideas import idea_repository

from . import idea_entities

import uuid
import arrow


def create_idea(owner, idea_for_create):
    idea = idea_entities.Idea(
        uuid = uuid.uuid4().hex,
        title = idea_for_create.title,
        description = idea_for_create.description,
        owner_id = owner.id,
        created_at = arrow.now(),
        is_public = idea_for_create.is_public,
        forked_from = None,
        comments_count = 0,
        reactions_counts = {},
    )
    return idea_repository.create(idea)


def list_ideas():
    ideas = idea_repository.list()
    return ideas

