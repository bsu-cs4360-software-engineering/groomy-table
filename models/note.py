from database import db

class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.String(100), nullable=False) # e.g., "client" or "employee"
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    appointment = db.relationship('Appointment', back_populates='notes')