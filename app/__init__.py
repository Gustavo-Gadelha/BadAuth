from flask import Flask, redirect
from flask_smorest import Api


def create_app() -> Flask:
    app = Flask(__name__)

    from app.config import Config
    app.config.from_object(Config)

    api = Api(app)

    from app import database
    database.create_all()

    from app import routes
    api.register_blueprint(routes.auth)
    app.add_url_rule('/', redirect_to='/api/v1/docs')

    return app
