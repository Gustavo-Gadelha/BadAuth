import sqlite3
from datetime import date

from app.config import SCHEMA_PATH, SQLITE_PATH

sqlite3.register_adapter(date, lambda date: date.isoformat())
sqlite3.register_converter('DATE', lambda b: date.fromisoformat(b.decode()))


def get_connection(path=SQLITE_PATH) -> sqlite3.Connection:
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    return con


def create_all() -> None:
    with get_connection() as con:
        create_tables(con)


def create_tables(con: sqlite3.Connection) -> None:
    schema = SCHEMA_PATH.read_text(encoding='utf-8')
    con.executescript(schema)
    con.commit()
