from cryptography.fernet import Fernet
from flask import Flask, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_smorest import Api
from werkzeug.exceptions import HTTPException

from app.config import TOKEN_KEY
from app.database import Database

db = Database()
api = Api()
fernet = Fernet(TOKEN_KEY)
limiter = Limiter(
    get_remote_address,
    storage_uri="redis://localhost:6379",
    storage_options={"socket_connect_timeout": 30},
    strategy="fixed-window", 
    )


def create_app() -> Flask:
    app = Flask(__name__)

    from app.config import Config

    app.config.from_object(Config)
    db.init_app(app)
    api.init_app(app)
    limiter.init_app(app)

    from app import routes

    api.register_blueprint(routes.auth)

    app.add_url_rule('/', endpoint='index', view_func=lambda: redirect('/api/v1/docs'))
    app.register_error_handler(HTTPException, lambda e: ({'message': e.description}, e.code))

    return app
