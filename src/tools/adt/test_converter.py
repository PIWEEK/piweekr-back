import pytest

from .types import ADT, Field
from .converter import to_plain, from_plain


class Point(ADT):
    x = Field(type=int)
    y = Field(type=int)
    z = Field(type=int, null=True)


class Vector(ADT):
    origin = Field(type=Point)
    angle = Field(type=float)
    modulus = Field()


def test_to_plain():
    p = Point(x=10, y=20)
    p_plain = to_plain(p)
    assert len(p_plain) == 3
    assert p_plain["x"] == 10
    assert p_plain["y"] == 20
    assert p_plain["z"] == None


def test_from_plain():
    p = from_plain(Point, {"x": 30, "y": 40})
    assert type(p) == Point
    assert p.x == 30
    assert p.y == 40
    assert p.z == None


def test_to_plain_complex():
    v = Vector(origin=Point(x=40, y=50, z=60), angle=45.0, modulus=100)
    v_plain = to_plain(v)
    assert len(v_plain) == 3
    assert v_plain["origin"]["x"] == 40
    assert v_plain["origin"]["y"] == 50
    assert v_plain["origin"]["z"] == 60
    assert v_plain["angle"] == 45.0
    assert v_plain["modulus"] == 100


def test_from_plain_complex():
    v = from_plain(Vector, {"origin": {"x": 30, "y": 40, "z": 50}, "angle": 120.5, "modulus": 33})
    assert type(v) == Vector
    assert v.origin.x == 30
    assert v.origin.y == 40
    assert v.origin.z == 50
    assert v.angle == 120.5
    assert v.modulus == 33

