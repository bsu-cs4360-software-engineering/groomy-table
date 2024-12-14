from database import db

class NoteLink(db.Model):
    __tablename__ = 'note_links'

    note_id = db.Column(db.Integer, db.ForeignKey('notes.id'), primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), default=None, nullable=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), default=None, nullable=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), default=None, nullable=True)

    note = db.relationship('Note', back_populates='links')
    customer = db.relationship('Customer', back_populates='note_links')
    appointment = db.relationship('Appointment', back_populates='note_links')
    service = db.relationship('Service', back_populates='note_links')

    __table_args__ = (
        db.CheckConstraint(
            'customer_id IS NOT NULL OR appointment_id IS NOT NULL OR service_id IS NOT NULL',
            name='check_note_link'),
    )