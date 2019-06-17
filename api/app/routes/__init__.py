from .views import views
from .db import apidb
from .api import api

def init_app(app):
    app.register_blueprint(views)
    app.register_blueprint(apidb, url_prefix='/db')
    app.register_blueprint(api, url_prefix='/api')
