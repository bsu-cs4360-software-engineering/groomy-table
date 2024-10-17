from database import db

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(20))
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    booked = db.Column(db.Boolean, default=False)

    places = db.relationship('Place', back_populates='appointment', cascade='all, delete-orphan')
    notes = db.relationship('Note', back_populates='appointment', cascade='all, delete-orphan')


# appointments = Appointment.query.all()
# for appointment in appointments:
#     for place in appointment.places:
#         print(place.address)