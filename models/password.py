from database import db

class UserPassword(db.Model):
    __tablename__ = 'user_password'

    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(250), nullable = False)