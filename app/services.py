# services.py
import json
from typing import Any

from werkzeug.exceptions import BadRequest, NotFound, Unauthorized

from app import db, fernet


class UserService:
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

        sql = 'SELECT * FROM users WHERE id = :user_id;'
        user = db.fetch_one(sql, {'user_id': user_id})
        if user is None:
            raise NotFound('Usuário não encontrado após criação')

        return self.generate_token(dict(user))

    def login(self, email: str, password: str):
        sql = 'SELECT * FROM users WHERE email = :email;'
        row = db.fetch_one(sql, {'email': email})
        if row is None:
            raise Unauthorized('Credenciais incorretas')

        user = dict(row)
        if user['password'] != password:
            raise Unauthorized('Credenciais incorretas')

        sql = """
            UPDATE users
            SET logged_in = 1
            WHERE id = :user_id;
        """

        db.execute(sql, {'user_id': user['id']})
        return self.generate_token(user['id'])

    def logout(self, token: str):
        sql = 'DELETE FROM tokens WHERE token = :token;'
        db.execute(sql, {'token': token})

    def get_current_user(self, token: str):
        sql = """
            SELECT u.* FROM users u
            JOIN tokens t ON u.id = t.user_id
            WHERE t.token = :token;
        """

        row = db.fetch_one(sql, {'token': token})
        if row is None:
            raise NotFound('Usuário não encontrado')

        return dict(row)

    def recover_password(self, document: str, email: str, new_password: str):
        sql = """
            SELECT * FROM users
            WHERE doc_number = :document AND email = :email;
        """

        row = db.fetch_one(sql, {'document': document, 'email': email})
        if row is None:
            raise NotFound('Usuário não encontrado com os dados fornecidos')

        sql = """
            UPDATE users
            SET password = :new_password
            WHERE id = :user_id;
        """

        user = dict(row)
        db.execute(sql, {'new_password': new_password, 'user_id': user['id']})

        return self.generate_token(user)

    def generate_token(self, user: dict[str, Any]):
        data = {'email': user['email'], 'doc_number': user['doc_number']}
        raw_bytes = json.dumps(data).encode()
        token = fernet.encrypt(raw_bytes).decode()

        sql = """
            SELECT 1 
            FROM tokens t
            WHERE t.token = :token;
        """

        if db.fetch_one(sql, {'token': token}):
            return token

        sql = """
            INSERT INTO tokens (token, user_id)
            VALUES (:token, :user_id);
        """

        db.execute(sql, {'token': token, 'user_id': user['id']})
        return token
