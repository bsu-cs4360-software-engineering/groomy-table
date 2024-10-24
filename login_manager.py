from flask_login import LoginManager

from models.user import User

login_manager = LoginManager()

login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))