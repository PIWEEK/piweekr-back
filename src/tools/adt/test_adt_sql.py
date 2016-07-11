import pytest

from .types import ADTID, Field, IntField, StrField
from .relationships import Relationship1N, RoleSingle, RoleMulti, Context
from sqlalchemy.sql import select, outerjoin

from .adt_sql import SQLADTRepository


class Card(ADTID):
    deck_id = IntField()
    title = StrField()
    strength = IntField()
    defense = IntField()


class Deck(ADTID):
    name = StrField()


class DeckHasCards(Relationship1N):
    role_1 = RoleSingle(role_class=Deck, role_name="deck")
    role_n = RoleMulti(role_class=Card, role_name="cards", role_fk="deck_id", required=False)


def test_sql_persistence():
    repo = SQLADTRepository({
        "DB_NAME": "test",
        "ECHO": False
    })

    repo.add_adt_table(Card, "cards")
    repo.add_adt_table(Deck, "decks")
    repo.create_all_tables()

    with repo.context() as context:

        deck = repo.insert_adt(context,
            repo.decks,
            Deck(
                name="Test deck"
            )
        )

        card_1 = repo.insert_adt(context,
            repo.cards,
            Card(
                deck_id=deck.id,
                title="Test card #1",
                strength=10,
                defense=1,
            )
        )

        card_2 = repo.insert_adt(context,
            repo.cards,
            Card(
                deck_id=deck.id,
                title="Test card #2",
                strength=8,
                defense=7,
            )
        )

    with repo.context() as context:

        r_deck = repo.retrieve_single_adt(context,
            Deck,
            select([repo.decks])
                .where(repo.decks.c.id == deck.id)
        )

    assert r_deck.id == deck.id
    assert r_deck.name == deck.name

    with repo.context() as context:

        r_decks = repo.retrieve_adts(context,
            {"decks": Deck, "cards": Card},
            select([repo.decks, repo.cards], use_labels=True)
                .select_from(outerjoin(
                    repo.decks, repo.cards, repo.decks.c.id == repo.cards.c.deck_id
                ))
                .where(repo.decks.c.id == deck.id)
        )

    assert len(r_decks) == 1

    r_deck = r_decks[0]
    assert r_deck.id == deck.id
    assert r_deck.name == deck.name

    assert len(context.cards(r_deck)) == 2
    assert card_1.id in [card.id for card in context.cards(r_deck)]
    assert card_2.id in [card.id for card in context.cards(r_deck)]

