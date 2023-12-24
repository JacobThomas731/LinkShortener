from flask import Flask
from LinkShortener.linkshortenerpackage.database import initialize_database
from LinkShortener.linkshortenerpackage.views import views

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.register_blueprint(views.views)
    return app


client = initialize_database()
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
