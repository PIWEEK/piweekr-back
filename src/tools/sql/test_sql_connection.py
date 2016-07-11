import pytest

from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Boolean, Text
from sqlalchemy.sql import select, insert, update, delete, func

from .sql_connection import SQLConnection


def test_sql():
    conn = SQLConnection({
        "DB_NAME": "test",
        "ECHO": False
    })

    conn.add_table("points", "test_points", [
        Column("id", Integer, primary_key=True),
        Column("x", Integer, nullable=False),
        Column("y", Integer, nullable=False),
        Column("z", Integer, nullable=True),
    ])

    conn.create_all_tables()
    with conn.session() as session:
        conn.truncate_table(session, conn.points)

    with conn.session() as session:
        point_id = conn.insert_into_table(
            session,
            insert(conn.points).values({
                "x": 10,
                "y": 20,
            })
        )

    assert point_id > 0

    with conn.session() as session:
        row_count = conn.update_table(
            session,
            update(conn.points).values({
                "z": 30,
            }).where(conn.points.c.id == point_id)
        )

    assert row_count == 1

    with conn.session() as session:
        row = conn.select_single_row(
            session,
            dict,
            select([conn.points])
                .where(conn.points.c.id == point_id)
        )

    assert row["x"] == 10
    assert row["y"] == 20
    assert row["z"] == 30

    with conn.session() as session:
        rows = conn.select_rows(
            session,
            dict,
            select([conn.points])
        )

    assert len(rows) == 1
    assert rows[0]["x"] == 10
    assert rows[0]["y"] == 20
    assert rows[0]["z"] == 30

    with conn.session() as session:
        row_count = conn.delete_from_table(
            session,
            delete(conn.points)
                .where(conn.points.c.id == point_id)
        )

    assert row_count == 1
