from datetime import datetime
from models.appointment import Appointment

def test_create_appointment(database):
    fixed_date = datetime(2024, 10, 25).date()
    fixed_time = datetime(2024, 10, 25, 14, 0).time()

    appointment = Appointment(
        client='John Doe',
        email='john@doe.com',
        phone_number='123-456-7890',
        date=fixed_date,
        time=fixed_time,
        booked=True
    )

    database.session.add(appointment)
    database.session.commit()

    assert appointment.id is not None
    assert appointment.client == 'John Doe'
    assert appointment.email == 'john@doe.com'
    assert appointment.phone_number == '123-456-7890'
    assert appointment.date == fixed_date
    assert appointment.time == fixed_time
    assert appointment.booked == True

def test_create_appointment_without_phone_number(database):
    fixed_date = datetime(2024, 10, 25).date()
    fixed_time = datetime(2024, 10, 25, 14, 0).time()

    appointment = Appointment(
        client='John Doe',
        email='john@doe.com',
        date=fixed_date,
        time=fixed_time,
        booked=True
    )

    database.session.add(appointment)
    database.session.commit()

    assert appointment.id is not None
    assert appointment.client == 'John Doe'
    assert appointment.phone_number is None

def test_booked_default_value(database):
    fixed_date = datetime(2024, 10, 25).date()
    fixed_time = datetime(2024, 10, 25, 14, 0).time()

    appointment = Appointment(
        client='John Doe',
        email='john@doe.com',
        date=fixed_date,
        time=fixed_time,
    )

    database.session.add(appointment)
    database.session.commit()

    assert appointment.id is not None
    assert appointment.client == 'John Doe'
    assert appointment.booked is False