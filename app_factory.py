import os
import stripe
from flask import Flask, render_template
from dotenv import load_dotenv

from models.service import Service

from routes.index import main as main_blueprint
from routes.auth import auth as auth_blueprint
from routes.dash import dash as dash_blueprint
from routes.appointment import appts as appts_blueprint
from routes.new_acc import new_acc as new_acc_blueprint

def create_app(database_uri="sqlite:///app.db"):
    load_dotenv()

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "TEMP_KEY"

    stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

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

def init_services():
    existing_services = Service.query.all()
    if not existing_services:
        services = [
            Service(
                name="Basic Grooming Package",
                description="Bath, brush, nail trim, ear cleaning, and drying.",
                # 50.00 - 70.00 (depending on dog size)
                price=60.00
            ),
            Service(
                name="Full Grooming Package",
                description="Everything in the Basic Grooming plus haircut/style.",
                # 75.00 - 100.00
                price=90.00
            ),
            Service(
                name="Puppy Package",
                description="Gentle bath, nail trim, and basic brush for puppies (up to 6 months).",
                price=40.00
            ),
            Service(
                name="Senior Dog Package",
                description="Gentle grooming services tailored for older dogs, focusing on comfort.",
                # 60.00 - 80.00
                price=70.00
            ),
            Service(
                name="De-shedding Treatment",
                # 20.00 - 30.00
                price=25.00,
                is_addon=True
            ),
            Service(
                name="Teeth Cleaning",
                price=15.00,
                is_addon=True
            ),
            Service(
                name="Flea/Tick Treatment",
                price=20.00,
                is_addon=True
            ),
            Service(
                name="Conditioning Treatment",
                price=15.00,
                is_addon=True
            ),
            # Service(
            #     name="Nail Dremel",
            #     price=10.00,
            #     is_addon=True
            # ),
            # Service(
            #     name="Specialty Shampoo (e.g., hypoallergenic, medicated)",
            #     price=10.00,
            #     is_addon=True
            # ),
            # Service(
            #     name="Basic Grooming + De-shedding Treatment",
            #     # 65.00 - 90.00 (depending on dog size)
            #     price=80.00,
            #     is_package=True
            # ),
            # Service(
            #     name="Full Grooming + Teeth Cleaning + Nail Dremel",
            #     # 100.00 - 130.00
            #     price=110.00,
            #     is_package=True
            # ),
            Service(
                name="Senior Dog Package + Flea/Tick Treatment",
                # 75.00 - 100.00
                price=85.00,
                is_package=True
            )
        ]
        
        return services
    
    return None