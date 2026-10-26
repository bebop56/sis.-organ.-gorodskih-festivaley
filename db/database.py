"""Подключение к базе данных SQLite проекта FestCity."""
import sqlite3
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "festcity.sqlite"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def get_connection(db_path=DB_PATH):
    """Открыть соединение с проверкой внешних ключей и доступом по именам."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_schema(conn):
    """Создать таблицы по файлу sql/schema.sql."""
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))


def _convert_dates(row):
    """sqlite3.Row → словарь; поля *_date из строк YYYY-MM-DD → date."""
    item = dict(row)
    for key, value in item.items():
        if key.endswith("_date") and isinstance(value, str):
            item[key] = date.fromisoformat(value)
    return item


def fetch_all(sql, params=()):
    """Выполнить параметризованный SELECT и вернуть все строки."""
    conn = get_connection()
    try:
        rows = conn.execute(sql, params).fetchall()
    finally:
        conn.close()
    return [_convert_dates(row) for row in rows]


def fetch_one(sql, params=()):
    """Выполнить параметризованный SELECT и вернуть одну строку или None."""
    conn = get_connection()
    try:
        row = conn.execute(sql, params).fetchone()
    finally:
        conn.close()
    return None if row is None else _convert_dates(row)
