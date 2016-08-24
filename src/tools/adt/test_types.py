import pytest

from .types import ADT, Field, StrField, IntField, ADT_WITH_ID


class Point(ADT):
    x = Field(type=int)
    y = Field(type=int)
    z = Field(type=int, null=True)

    def move_horizontal(self, distance):
        self.x = self.x + distance

    def bad_method(self):
        self.a = 0

    def other_bad_method(self):
        self.x = "hey"


def test_adt():
    with pytest.raises(AssertionError):
        p = Point(x = 10)

    p = Point(x = 10, y = 20)
    assert p.x == 10
    assert p.z == None

    p.move_horizontal(5)
    assert p.x == 15

    with pytest.raises(NotImplementedError):
        p.x = 30

    with pytest.raises(IndexError):
        p.bad_method()

    with pytest.raises(AssertionError):
        p.other_bad_method()


class Mineral(ADT_WITH_ID):
    name = StrField()
    description = StrField()
    hardness = IntField()


def test_adt_id():
    m = Mineral(name="yoyoyo", description="yayayaya", hardness=3)

    assert m.id is None
    assert not m.is_attached

    m.attach(3)
    assert m.id == 3
    assert m.is_attached

