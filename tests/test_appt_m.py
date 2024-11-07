from datetime import datetime
from models.appointment import Appointment

def test_create_appointment(database):
    fixed_date = datetime(2024, 10, 25).date()
    fixed_time = datetime(2024, 10, 25, 14, 0).time()

    appointment = Appointment(
        date=fixed_date,
        time=fixed_time,
        booked=True
    )

    database.session.add(appointment)
    database.session.commit()

    assert appointment.id is not None
    assert appointment.date == fixed_date
    assert appointment.time == fixed_time
    assert appointment.booked == True

def test_booked_default_value(database):
    fixed_date = datetime(2024, 10, 25).date()
    fixed_time = datetime(2024, 10, 25, 14, 0).time()

    appointment = Appointment(
        date=fixed_date,
        time=fixed_time,
    )

    database.session.add(appointment)
    database.session.commit()

    assert appointment.id is not None
    assert appointment.booked is False