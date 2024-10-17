from app_factory import create_app
from database import db

app = create_app()

# Initialize the database with the app
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)