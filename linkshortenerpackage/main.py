from flask import Flask
from database import initialize_database

def create_app():
    app = Flask(__name__, template_folder='templates')
    from views import views

    app.register_blueprint(views.views)
    return app


client = initialize_database()
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
