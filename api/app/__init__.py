from flask import Flask
from flask_migrate import Migrate
from .config import config
from flask_cors import CORS

migrate = Migrate()


def create_app():
    from . import models, routes
    app = Flask(__name__)
    app.config.from_object(config)

    models.init_app(app)
    routes.init_app(app)
    migrate.init_app(app, models)
    CORS(app)
    return app


app = create_app()
