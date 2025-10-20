from flask_smorest import Blueprint

from app.schemas import AuthorizationSchema, LoginSchema, RecoverPasswordSchema, TokenSchema, UserSchema
from app.services import UserService

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/signup', methods=['POST'])
@auth.arguments(UserSchema, location='json')
@auth.response(200, TokenSchema)
@auth.response(400)
def signup(schema, user_service: UserService):
    return user_service.create_user(schema)


@auth.route('/login', methods=['POST'])
@auth.arguments(LoginSchema, location='json')
@auth.response(200, TokenSchema)
@auth.alt_response(400)
def login(schema, user_service: UserService):
    login = schema.get('login')
    password = schema.get('password')
    return user_service.login(login, password)


@auth.route('/logout', methods=['POST'])
@auth.arguments(AuthorizationSchema, location='headers')
@auth.response(200)
@auth.alt_response(400)
def logout(schema, user_service: UserService):
    token = schema.get('authorization')
    return user_service.logout(token)


@auth.route('/recuperar-senha', methods=['POST'])
@auth.arguments(RecoverPasswordSchema, location='json')
@auth.response(200, TokenSchema)
@auth.alt_response(404)
def recuperar_senha(schema, user_service: UserService):
    document = schema.get('document')
    email = schema.get('email')
    new_password = schema.get('new_password')
    return user_service.recover_password(document, email, new_password)


@auth.route('/me', methods=['GET'])
@auth.arguments(AuthorizationSchema, location='headers')
@auth.response(200, UserSchema)
@auth.alt_response(404)
def me(schema, user_service: UserService):
    token = schema.get('authorization')
    return user_service.get_current_user(token)
