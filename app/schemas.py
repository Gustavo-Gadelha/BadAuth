# schemas.py

from marshmallow import Schema, fields


class UserSchema(Schema):
    full_name = fields.Str(required=True)
    email = fields.Email(required=True)
    doc_number = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    logged_in = fields.Bool(dump_only=True)
    created_at = fields.Str(dump_only=True)
    updated_at = fields.Str(dump_only=True)


class TokenSchema(Schema):
    token = fields.Str(dump_only=True, required=True)


class LoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class RecoverPasswordSchema(Schema):
    document = fields.Str(required=True)
    email = fields.Email(required=True)
    new_password = fields.Str(required=True)
