from flask import Flask, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.exceptions import HTTPException
from flask_smorest import Api

from app.database import Database

db = Database()
api = Api()
limiter = Limiter(get_remote_address)


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

    @app.errorhandler(HTTPException) # type: ignore
    def handle_exception(e: HTTPException):
        return {'message': e.description}, e.code
    
    return app
