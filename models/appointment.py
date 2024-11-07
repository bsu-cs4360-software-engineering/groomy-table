from database import db

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    booked = db.Column(db.Boolean, default=False)

    customer = db.relationship('Customer', back_populates='appointments')
    note_links = db.relationship('NoteLink', back_populates='appointment', cascade='all, delete-orphan')