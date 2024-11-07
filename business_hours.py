from datetime import time

from models.business_hours import BusinessHours, DayOfWeek

def create_hours(db):
    business_days = [
        BusinessHours(
            start_time=time(9, 0),
            end_time=time(17, 0),
            appt_length_minutes=90,
            day_of_week=DayOfWeek.MONDAY
        ),
        BusinessHours(
            start_time=time(9, 0),
            end_time=time(17, 0),
            appt_length_minutes=90,
            day_of_week=DayOfWeek.TUESDAY
        ),
        BusinessHours(
            start_time=time(9, 0),
            end_time=time(17, 0),
            appt_length_minutes=90,
            day_of_week=DayOfWeek.WEDNESDAY
        ),
        BusinessHours(
            start_time=time(9, 0),
            end_time=time(17, 0),
            appt_length_minutes=90,
            day_of_week=DayOfWeek.THURSDAY
        ),
        BusinessHours(
            start_time=time(9, 0),
            end_time=time(17, 0),
            appt_length_minutes=90,
            day_of_week=DayOfWeek.FRIDAY
        ),
        BusinessHours(
            start_time=time(9, 0),
            end_time=time(17, 0),
            appt_length_minutes=90,
            day_of_week=DayOfWeek.SATURDAY
        ),
        BusinessHours(
            start_time=time(11, 0),
            end_time=time(17, 0),
            appt_length_minutes=90,
            day_of_week=DayOfWeek.SUNDAY
        )
    ]

    for business_hour in business_days:
        existing_hours = db.session.query(BusinessHours).filter_by(day_of_week=business_hour.day_of_week).first()
        if not existing_hours:
            db.session.add(business_hour)

    db.session.commit()