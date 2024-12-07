from database import db
from datetime import datetime

class Invoice(db.Model):
    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), default=1)
    provider_address = db.Column(db.String(255), default="Bemidji", nullable=False)
    customer_address = db.Column(db.String(255), nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), default = 0.00, nullable=False)
    paid = db.Column(db.Boolean, default=False, nullable=False)
    booked = db.Column(db.Boolean, default=False, nullable=False)
    deleted = db.Column(db.Boolean, default=False, nullable=False)

    user = db.relationship('User', back_populates='invoices')