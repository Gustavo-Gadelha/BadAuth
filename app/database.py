import sqlite3
from datetime import date
from pathlib import Path

from flask import Flask, g

from app.config import SCHEMA_PATH, SQLITE_PATH

sqlite3.register_adapter(date, lambda date: date.isoformat())
sqlite3.register_converter('DATE', lambda b: date.fromisoformat(b.decode()))


class Database:
    def __init__(
        self, app: Flask | None = None, *, db_path: str | Path = SQLITE_PATH, schema_path: str | Path = SCHEMA_PATH
    ) -> None:
        self.db_path = Path(db_path)
        self.schema_path = Path(schema_path)

        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        app.teardown_appcontext(self.close_connection)
        with app.app_context():
            self.create_all()

    def get_connection(self) -> sqlite3.Connection:
        if '_conn' not in g:
            con = sqlite3.connect(self.db_path)
            con.row_factory = sqlite3.Row
            g._conn = con

        return g._conn

    def close_connection(self, exception) -> None:
        con = g.pop('_conn', None)
        if con is not None:
            con.close()

    def create_all(self) -> None:
        with self.get_connection() as con:
            schema = self.schema_path.read_text(encoding='utf-8')
            con.executescript(schema)
            con.commit()

    def fetch_one(self, sql: str, params=()) -> sqlite3.Row | None:
        with self.get_connection() as con:
            cur = con.execute(sql, params)
        try:
            return cur.fetchone()
        finally:
            cur.close()

    def fetch_all(self, sql: str, params=()) -> list[sqlite3.Row]:
        with self.get_connection() as con:
            cur = con.execute(sql, params)
        try:
            return cur.fetchall()
        finally:
            cur.close()

    def execute(self, sql: str, params=(), *, many: bool = False) -> int | None:
        with self.get_connection() as con:
            if many:
                cur = con.executemany(sql, params)
            else:
                cur = con.execute(sql, params)
        try:
            return cur.lastrowid
        finally:
            cur.close()
