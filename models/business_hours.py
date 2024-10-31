from database import db

class BusinessHours(db.Model):
    __tablename__ = 'business_hours'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    appt_length_minutes = db.Column(db.Integer, nullable=False)
    day_of_week = db.Column(db.String(9))