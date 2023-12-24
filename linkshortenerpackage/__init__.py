from flask import Flask

from . import database
from .views import views


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.register_blueprint(views.views)
    client = database.initialize_database()
    print(client)

    return app
