from flask import Flask

from LinkShortener.linkshortenerpackage import database
from LinkShortener.linkshortenerpackage.views import views

def create_app():
    app = Flask(__name__, template_folder='linkshortenerpackage/templates', static_folder='linkshortenerpackage/static')
    app.register_blueprint(views.views)
    return app


client = database.initialize_database()
print(client)
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
