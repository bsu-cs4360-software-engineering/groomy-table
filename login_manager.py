from flask_login import LoginManager

from database import db
from models.user import User

login_manager = LoginManager()

login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return db.query(User).get(int(user_id))