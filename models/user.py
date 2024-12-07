from flask_login import UserMixin
from database import db

class User(UserMixin, db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_id = db.Column(db.Integer, db.ForeignKey('user_password.id'))

    password = db.relationship('UserPassword', backref='user', uselist=False) #adds bi-directional access between classes and makes it one-to-one
    invoices = db.relationship('Invoice', back_populates='user', cascade='all, delete-orphan')