"""Перенос данных FestCity из JSON-файлов в базу SQLite.

Запуск из корня проекта: python -m db.import_json
"""
import json

from db.database import BASE_DIR, DB_PATH, create_schema, get_connection

DATA_DIR = BASE_DIR / "data"


def load_json(filename):
    with open(DATA_DIR / filename, encoding="utf-8") as file:
        return json.load(file)


def import_venues(conn):
    venues = load_json("venues.json")
    conn.executemany(
        """
        INSERT INTO venues (id, name, address, capacity)
        VALUES (?, ?, ?, ?)
        """,
        [
            (v["id"], v["name"], v.get("address"), v["capacity"])
            for v in venues
        ],
    )


def import_organizers(conn):
    organizers = load_json("organizers.json")
    conn.executemany(
        """
        INSERT INTO organizers (id, name, email)
        VALUES (?, ?, ?)
        """,
        [(o["id"], o["name"], o["email"]) for o in organizers],
    )


def import_festivals(conn):
    festivals = load_json("festivals.json")
    conn.executemany(
        """
        INSERT INTO festivals (
            id, title, venue_id, organizer_id,
            festival_date, expected_visitors, is_cancelled
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                f["id"],
                f["title"],
                f["venue_id"],
                f["organizer_id"],
                f["festival_date"],
                f["expected_visitors"],
                int(f["is_cancelled"]),
            )
            for f in festivals
        ],
    )


def import_all(db_path=DB_PATH):
    """Создать схему и заново заполнить таблицы данными из JSON."""
    conn = get_connection(db_path)
    try:
        create_schema(conn)
        # Повторный импорт: сначала зависимая таблица, затем справочники.
        conn.execute("DELETE FROM festivals")
        conn.execute("DELETE FROM organizers")
        conn.execute("DELETE FROM venues")
        # Порядок важен: фестивали ссылаются на площадки и организаторов.
        import_venues(conn)
        import_organizers(conn)
        import_festivals(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def main():
    import_all()
    conn = get_connection()
    counts = conn.execute(
        """
        SELECT
            (SELECT COUNT(*) FROM venues) AS venues,
            (SELECT COUNT(*) FROM organizers) AS organizers,
            (SELECT COUNT(*) FROM festivals) AS festivals
        """
    ).fetchone()
    conn.close()
    for table in counts.keys():
        print(f"{table}: {counts[table]}")


if __name__ == "__main__":
    main()
