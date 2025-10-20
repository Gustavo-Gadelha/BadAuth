import sqlite3

from flask import Flask
from flask_injector import request

from injector import Module, provider


class SqliteModule(Module):
    @provider
    @request
    def provide_db_connection(self, app: Flask) -> sqlite3.Connection:
        from app.database import get_connection

        return get_connection()
