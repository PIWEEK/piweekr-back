from sqlalchemy.sql import select, outerjoin
from tools.adt.adt_sql import SQLADTRepository

from core.ideas import idea_entities

from services.repository.sql import repo

repo.add_adt_table(idea_entities.Idea, "ideas")


def create(idea):
    with repo.context() as context:
        idea = repo.insert_adt(context, repo.ideas, idea)
    return idea


