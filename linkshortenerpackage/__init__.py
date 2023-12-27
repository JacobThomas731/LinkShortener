from flask import Flask

from . import database
from .views import views


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.register_blueprint(views.views)
    app.register_error_handler(404, views.page_not_found)
    app.register_error_handler(500, views.page_not_found)
    client = database.initialize_database()

    return app
