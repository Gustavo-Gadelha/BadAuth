# schemas.py
from marshmallow import Schema, fields


class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class RecuperarSenhaSchema(Schema):
    document = fields.Str(required=True)
    email = fields.Email(required=True)
    new_password = fields.Str(required=True)


class TokenSchema(Schema):
    user_id = fields.Int(dump_only=True)
    token = fields.Str(required=True)
    created_at = fields.Date(format='iso')


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    full_name = fields.Str(required=True)
    email = fields.Email(required=True)
    doc_number = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    logged_in = fields.Bool()
    created_at = fields.Date(format='iso')
    updated_at = fields.Date(format='iso')
