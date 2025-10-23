import sqlite3
from datetime import date

from flask import Flask, g

from app.config import SCHEMA_PATH, SQLITE_PATH

sqlite3.register_adapter(date, lambda date: date.isoformat())
sqlite3.register_converter('DATE', lambda b: date.fromisoformat(b.decode()))


def init_database(app: Flask) -> None:
    app.teardown_appcontext(close_connection)
    with app.app_context():
        create_all()


def get_connection(path=SQLITE_PATH) -> sqlite3.Connection:
    if 'con' not in g:
        g.con = sqlite3.connect(path)
        g.con.row_factory = sqlite3.Row

    return g.con


def close_connection(exception):
    con = g.pop('con', None)
    if con is not None:
        con.close()


def create_all() -> None:
    with get_connection() as con:
        schema = SCHEMA_PATH.read_text(encoding='utf-8')
        con.executescript(schema)
        con.commit()
