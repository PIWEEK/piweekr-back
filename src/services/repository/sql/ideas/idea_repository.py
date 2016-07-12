from sqlalchemy.sql import select, outerjoin
from tools.adt.adt_sql import SQLADTRepository

from core.ideas import idea_entities
from core.users import user_entities

from services.repository.sql import repo

repo.add_adt_table(idea_entities.Idea, "ideas")


def create(idea):
    with repo.context() as context:
        idea = repo.insert_adt(context, repo.ideas, idea)
    return idea


def list():
    with repo.context() as context:
        ideas = repo.retrieve_joined_adts(context,
            idea_entities.Idea, {"ideas": idea_entities.Idea, "users": user_entities.User},
            select([repo.ideas, repo.users], use_labels=True)
                .select_from(outerjoin(
                    repo.ideas, repo.users, repo.ideas.c.owner_id == repo.users.c.id
                ))
                .order_by(repo.ideas.c.title)
        )
    return ideas

