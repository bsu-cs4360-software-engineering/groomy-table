from enum import Enum
from database import db

class AppointmentStatus(Enum):
    OPEN = "OPEN" # Appointment is available for booking; the user can accept.
    CLOSED = "CLOSED" # Time slot is no longer available (e.g., double-booked).
    BOOKED = "BOOKED" # Appointment has been confirmed.
    COMPLETE = "COMPLETE" # Appointment has been completed
    DELETED = "DELETED" # Appointment has been deleted by the user.

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    payed = db.Column(db.Boolean, default=False, nullable=False)
    status = db.Column(db.Enum(AppointmentStatus), default=AppointmentStatus.OPEN, nullable=False)
    payment_intent_id = db.Column(db.String(100), nullable=True)

    customer = db.relationship('Customer', back_populates='appointments')
    note_links = db.relationship('NoteLink', back_populates='appointment', cascade='all, delete-orphan')