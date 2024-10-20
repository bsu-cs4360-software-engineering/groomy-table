from flask import Flask

from routes.index import main as main_blueprint
# from routes.auth import auth as auth_blueprint
# from routes.dash import dash as dash_blueprint
# from routes.appointment import appts as appts_blueprint

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "TEMP_KEY"

    # Register blueprints
    app.register_blueprint(main_blueprint)
    # app.register_blueprint(auth_blueprint)
    # app.register_blueprint(dash_blueprint)
    # app.register_blueprint(appts_blueprint)

    return app