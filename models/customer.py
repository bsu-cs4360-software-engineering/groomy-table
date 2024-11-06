from database import db

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(20))

    note_links = db.relationship('NoteLink', back_populates='customer', cascade='all, delete-orphan')
    places = db.relationship('Place', back_populates='customer', cascade='all, delete-orphan')
    appointments = db.relationship('Appointment', back_populates='customer', cascade='all, delete-orphan')