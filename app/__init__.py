from flask import Flask, redirect
from flask_smorest import Api
from limits import parse, storage, strategies
from werkzeug.exceptions import HTTPException

from app.database import Database

limits_storage = storage.MemoryStorage()
limiter = strategies.FixedWindowRateLimiter(limits_storage)

db = Database()
api = Api()


def create_app() -> Flask:
    app = Flask(__name__)

    from app.config import Config

    app.config.from_object(Config)
    db.init_app(app)
    api.init_app(app)

    from app import routes

    api.register_blueprint(routes.auth)
    app.add_url_rule('/', endpoint='index', view_func=lambda: redirect('/api/v1/docs'))

    @app.errorhandler(HTTPException)  # type: ignore
    def handle_exception(e: HTTPException):
        return {'message': e.description}, e.code

    return app
