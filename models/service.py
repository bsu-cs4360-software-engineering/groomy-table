from database import db

class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(55), nullable=False, unique=True)
    description = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    is_addon = db.Column(db.Boolean, default=False)
    is_package = db.Column(db.Boolean, default=False)
    deleted = db.Column(db.Boolean, default=False, nullable=False)

    note_links = db.relationship('NoteLink', back_populates='service', cascade='all, delete-orphan')