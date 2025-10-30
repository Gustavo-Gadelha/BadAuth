from flask import request
from flask_smorest import Blueprint
from werkzeug.exceptions import BadRequest

from app import limiter
from app.schemas import LoginSchema, RecoverPasswordSchema, TokenSchema, UserSchema
from app.services import UserService

auth = Blueprint('auth', __name__, url_prefix='/auth')
user_service = UserService.instance()


@auth.route('/signup', methods=['POST'])
@auth.arguments(UserSchema, location='json')
@auth.response(200, TokenSchema)
@auth.response(400)
def signup(schema):
    token = user_service.create_user(schema)
    return {'token': token}, 200


@auth.route('/login', methods=['POST'])
@limiter.limit('3 per 10 minutes')
@auth.arguments(LoginSchema, location='json')
@auth.response(200, TokenSchema)
@auth.alt_response(400)
def login(schema):
    login = schema.get('login')
    password = schema.get('password')
    token = user_service.login(login, password)
    return {'token': token}, 200


@auth.route('/logout', methods=['POST'])
@auth.response(200)
@auth.alt_response(401)
def logout():
    token = request.headers.get('Authorization')
    if token is None:
        return BadRequest('Token de autenticação é obrigatório'), 401

    return user_service.logout(token)


@auth.route('/recuperar-senha', methods=['POST'])
@auth.arguments(RecoverPasswordSchema, location='json')
@auth.response(200, TokenSchema)
@auth.alt_response(404)
def recuperar_senha(schema):
    document = schema.get('document')
    email = schema.get('email')
    new_password = schema.get('new_password')
    token = user_service.recover_password(document, email, new_password)
    return {'token': token}, 200


@auth.route('/me', methods=['GET'])
@limiter.limit('3 per 10 minutes')
@auth.response(200, UserSchema)
@auth.alt_response(401)
def me():
    token = request.headers.get('Authorization')
    if token is None:
        return BadRequest('Token de autenticação é obrigatório'), 401

    return user_service.get_current_user(token), 200
