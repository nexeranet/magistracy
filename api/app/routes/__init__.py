from .views import views 
from .db import apidb
def init_app(app):
    app.register_blueprint(views)
    app.register_blueprint(apidb, url_prefix='/db')
