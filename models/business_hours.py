from enum import Enum

from sqlalchemy import CheckConstraint
from sqlalchemy import Enum as SQLAlchemyEnum

from database import db

class DayOfWeek(Enum):
    MONDAY = "Monday",
    TUESDAY = "Tuesday",
    WEDNESDAY = "Wednesday",
    THURSDAY = "Thursday",
    FRIDAY = "Friday",
    SATURDAY = "Saturday",
    SUNDAY = "Sunday"

class BusinessHours(db.Model):
    __tablename__ = 'business_hours'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    appt_length_minutes = db.Column(db.Integer, nullable=False)
    day_of_week = db.Column(SQLAlchemyEnum(DayOfWeek, name="day_of_week_enum"), nullable=False)
    is_closed = db.Column(db.Boolean, default=False)

    __table__args = (
        CheckConstraint('start_time < end_time', name='check_start_before_end')
    )