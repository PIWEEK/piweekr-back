import pytest

from .types import ADTID, Field, IntField, StrField
from .relationships import Relationship1N, RoleSingle, RoleMulti, Context


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


def test_meta():
    assert Card._relationships["deck"] == DeckHasCards
    assert Deck._relationships["cards"] == DeckHasCards


def test_relationships():
    context = Context()

    d = Deck(
        id=1,
        name="Test deck"
    )
    context.add(d)

    c1 = Card(
        id=1,
        deck_id=d.id,
        title="Test card #1",
        strength=10,
        defense=1,
    )
    context.add(c1)

    c2 = Card(
        id=2,
        deck_id=d.id,
        title="Test card #2",
        strength=8,
        defense=7,
    )
    context.add(c2)

    assert context.deck(c1) == d
    assert len(context.cards(d)) == 2
    assert context.cards(d)[0] == c1
    assert context.cards(d)[1] == c2

