from .views import views
from .db import apidb
from .api import api
from flask import redirect

def init_app(app):

    @app.errorhandler(404)
    def page_not_found(e):
        return redirect('/', 302)

    app.register_blueprint(views)
    app.register_blueprint(apidb, url_prefix='/db')
    app.register_blueprint(api, url_prefix='/api')
