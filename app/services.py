import json
from typing import Any

from werkzeug.exceptions import BadRequest, NotFound, Unauthorized

from app import db, fernet


class UserService:
    def get_user_by_email(self, email: str):
        sql = """
            SELECT * FROM users WHERE email = ?;
        """
        row = db.fetch_one(sql, (email,))
        return dict(row) if row else None

    def get_user_by_token(self, token: str):
        sql = """
            SELECT u.*
            FROM users u
            JOIN tokens t ON u.id = t.user_id
            WHERE t.token = ?;
        """
        row = db.fetch_one(sql, (token,))
        return dict(row) if row else None

    def user_exists(self, email: str, doc_number: str):
        sql = """
            SELECT 1
            FROM users
            WHERE email = ? OR doc_number = ?
            LIMIT 1;
        """
        row = db.fetch_one(sql, (email, doc_number))
        return row is not None

    def create_user(self, schema: dict[str, Any]):
        if self.user_exists(schema['email'], schema['doc_number']):
            raise BadRequest('Usuário com este email ou documento já existe')

        sql = """
            INSERT INTO users (full_name, email, doc_number, username, password)
            VALUES (:full_name, :email, :doc_number, :username, :password);
        """
        user_id = db.execute(sql, schema)

        sql = 'SELECT * FROM users WHERE id = ?;'
        row = db.fetch_one(sql, (user_id,))
        if row is None:
            raise Exception('Erro ao criar usuário')

        return self.generate_token(dict(row))

    def login(self, email: str, password: str):
        user = self.get_user_by_email(email)
        if user is None:
            raise Unauthorized('Credenciais incorretas')
        if user['password'] != password:
            raise Unauthorized('Credenciais incorretas')

        sql = """
            UPDATE users
            SET logged_in = 1
            WHERE id = ?;
        """
        db.execute(sql, (user['id'],))

        return self.generate_token(user)

    def logout(self, token: str) -> None:
        sql = 'DELETE FROM tokens WHERE token = ?;'
        db.execute(sql, (token,))

    def get_current_user(self, token: str):
        user = self.get_user_by_token(token)
        if user is None:
            raise NotFound('Usuário não encontrado')
        return user

    def recover_password(self, document: str, email: str, new_password: str):
        sql = """
            SELECT *
            FROM users
            WHERE doc_number = ? AND email = ?;
        """
        row = db.fetch_one(sql, (document, email))

        if row is None:
            raise NotFound('Usuário não encontrado')

        user = dict(row)

        sql = """
            UPDATE users
            SET password = ?
            WHERE id = ?;
        """
        db.execute(sql, (new_password, user['id']))

        return self.generate_token(user)

    def generate_token(self, user: dict[str, Any]):
        data = {'email': user['email'], 'doc_number': user['doc_number']}
        raw_bytes = json.dumps(data).encode()
        token = fernet.encrypt(raw_bytes).decode()

        sql = """
            SELECT 1
            FROM tokens
            WHERE token = ?;
        """

        if db.fetch_one(sql, (token,)):
            return token

        sql = """
            INSERT INTO tokens (token, user_id)
            VALUES (?, ?);
        """
        db.execute(sql, (token, user['id']))

        return token
