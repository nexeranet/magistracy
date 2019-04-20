from .views import views 
def init_app(app):
    app.register_blueprint(views)
