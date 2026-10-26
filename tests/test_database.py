"""Тесты слоя базы данных SQLite (ПР7)."""
import json
import sqlite3

import pytest

from db.database import get_connection
from db.import_json import DATA_DIR, import_all


@pytest.fixture
def conn(tmp_path):
    db_path = tmp_path / "test.sqlite"
    import_all(db_path)
    connection = get_connection(db_path)
    yield connection
    connection.close()


def json_count(filename):
    with open(DATA_DIR / filename, encoding="utf-8") as file:
        return len(json.load(file))


def test_tables_created(conn):
    tables = {
        row["name"]
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )
    }
    assert {"venues", "organizers", "festivals"} <= tables


def test_import_matches_json(conn):
    counts = conn.execute(
        """
        SELECT
            (SELECT COUNT(*) FROM venues) AS venues,
            (SELECT COUNT(*) FROM organizers) AS organizers,
            (SELECT COUNT(*) FROM festivals) AS festivals
        """
    ).fetchone()
    assert counts["venues"] == json_count("venues.json")
    assert counts["organizers"] == json_count("organizers.json")
    assert counts["festivals"] == json_count("festivals.json")


def test_import_is_repeatable(tmp_path):
    db_path = tmp_path / "twice.sqlite"
    import_all(db_path)
    import_all(db_path)
    connection = get_connection(db_path)
    count = connection.execute("SELECT COUNT(*) FROM venues").fetchone()[0]
    connection.close()
    assert count == json_count("venues.json")


def test_foreign_keys_enforced(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            """
            INSERT INTO festivals (
                title, venue_id, organizer_id,
                festival_date, expected_visitors
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            ["Несуществующая площадка", 999, 1, "2027-01-01", 10],
        )


def test_free_venues_query_excludes_busy(conn):
    rows = conn.execute(
        """
        SELECT venues.name
        FROM venues
        WHERE venues.capacity >= ?
          AND venues.id NOT IN (
              SELECT venue_id FROM festivals
              WHERE festival_date = ? AND is_cancelled = 0
          )
        """,
        [1000, "2026-11-14"],
    ).fetchall()
    names = [row["name"] for row in rows]
    assert "Парк Горького" not in names
    assert "Площадь Революции" in names


def test_cancelled_festival_does_not_block_venue(conn):
    busy = conn.execute(
        """
        SELECT COUNT(*) FROM festivals
        WHERE venue_id = ? AND festival_date = ? AND is_cancelled = 0
        """,
        [1, "2026-11-07"],
    ).fetchone()[0]
    assert busy == 0
