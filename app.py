from app_factory import create_app
from login_manager import login_manager
from database import db

app = create_app()

login_manager.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)