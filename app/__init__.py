from flask import Flask, redirect
from flask_smorest import Api


def create_app() -> Flask:
    from flask_injector import FlaskInjector
    app = Flask(__name__)

    from app.config import Config
    app.config.from_object(Config)

    api = Api(app)

    from app import database
    database.create_all()

    from app import routes
    api.register_blueprint(routes.auth)

    from app import injector
    FlaskInjector(app=app, modules=[injector.SqliteModule()])

    app.add_url_rule('/', endpoint='index', view_func=lambda: redirect('/api/v1/docs'))

    return app
