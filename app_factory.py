from flask import Flask

from routes.index import main as main_blueprint
from routes.auth import auth as auth_blueprint
from routes.dash import dash as dash_blueprint
from routes.appointment import appts as appts_blueprint
from routes.new_acc import new_acc as new_acc_blueprint

def create_app(database_uri="sqlite:///app.db"):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "TEMP_KEY"

    # Register blueprints
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(dash_blueprint)
    app.register_blueprint(appts_blueprint)
    app.register_blueprint(new_acc_blueprint)

    return app