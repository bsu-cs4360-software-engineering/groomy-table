from datetime import datetime
from models.appointment import Appointment, AppointmentStatus
from models.customer import Customer

def test_create_appointment(database):
    fixed_date = datetime(2024, 10, 25).date()
    fixed_time = datetime(2024, 10, 25, 14, 0).time()

    test_customer = database.query(Customer).first()

    assert test_customer is not None, "Test customer was not found in the database."

    appointment = Appointment(
        customer_id=test_customer.id,
        date=fixed_date,
        time=fixed_time
    )

    database.add(appointment)
    database.commit()

    assert appointment.id is not None
    assert appointment.customer.id == test_customer.id
    assert appointment.date == fixed_date
    assert appointment.time == fixed_time
    assert appointment.payed == False
    assert appointment.status == AppointmentStatus.OPEN

def test_status_value(database):
    fixed_date = datetime(2024, 10, 25).date()
    fixed_time = datetime(2024, 10, 25, 14, 0).time()

    test_customer = database.query(Customer).first()

    assert test_customer is not None, "Test customer was not found in the database."

    appointment = Appointment(
        customer_id=test_customer.id,
        date=fixed_date,
        time=fixed_time,
        status=AppointmentStatus.COMPLETE
    )

    database.add(appointment)
    database.commit()

    assert appointment.id is not None
    assert appointment.status is AppointmentStatus.COMPLETE