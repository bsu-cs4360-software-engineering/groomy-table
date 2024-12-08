from app_factory import create_app, init_services
from login_manager import login_manager
from business_hours import create_hours
from database import db

app = create_app()

# Initialize the database with the app
db.init_app(app)

login_manager.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()
    create_hours(db)

    services = init_services()
    if services is not None:
        db.session.bulk_save_objects(services)
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)