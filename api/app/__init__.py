from flask import Flask
from flask_migrate import Migrate
from .config import config

def create_app():
    from . import models, routes
    app = Flask(__name__)
    app.config.from_object(config)

    models.init_app(app)
    routes.init_app(app)

    return app

app = create_app()
