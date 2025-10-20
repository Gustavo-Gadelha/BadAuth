# services.py
from __future__ import annotations

import base64
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import sqlite3

    from app.models import User


class UserService:
    def __init__(self, db: sqlite3.Connection):
        self._db = db

    def user_exists(self, username: str, email: str, doc_number: str):
        pass

    def create_user(self, user: User):
        pass

    def login(self, username: str, password: str):
        pass

    def logout(self, token: str):
        pass

    def get_current_user(self, token: str):
        pass

    def recover_password(self, document: str, email: str, new_password: str):
        pass

    def _make_token(self, email: str, doc_number: str):
        raw = f'{email}:{doc_number}'.encode()
        tok = base64.urlsafe_b64encode(raw).decode('utf-8')
        return tok.rstrip('=')
