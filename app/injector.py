from typing import TYPE_CHECKING

from flask_injector import request

from injector import Module, provider

if TYPE_CHECKING:
    import sqlite3

    from flask import Flask


class SqliteModule(Module):
    @request
    @provider
    def provide_db_connection(self, app: Flask) -> sqlite3.Connection:
        from app.database import get_connection

        return get_connection()
