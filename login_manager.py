from flask_login import LoginManager
from werkzeug.security import generate_password_hash

from models.user import User

login_manager = LoginManager()

login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_first_user(db):
    username = "admin"
    email = "admin@example.com"
    password = "securepassword"

    if not User.query.filter_by(username=username).first():
        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(new_user)
        db.session.commit()