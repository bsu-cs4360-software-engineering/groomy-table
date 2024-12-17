import os
import stripe
from flask import Flask, render_template
from dotenv import load_dotenv

def create_app(database_uri="sqlite:///app.db"):
    from database import db

    load_dotenv()

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "TEMP_KEY"

    stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

    db.init_db(app)

    from routes.index import main as main_blueprint
    from routes.auth import auth as auth_blueprint
    from routes.dash import dash as dash_blueprint
    from routes.appointment import appts as appts_blueprint
    from routes.new_acc import new_acc as new_acc_blueprint

    # Register blueprints
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(dash_blueprint)
    app.register_blueprint(appts_blueprint)
    app.register_blueprint(new_acc_blueprint)

    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    return app