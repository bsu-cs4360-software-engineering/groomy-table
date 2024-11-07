from models.customer import Customer

def test_create_customer(database):
    customer = Customer(
        name='John Doe',
        email='john.doe@email.org',
        phone_number='123-456-7890'
    )

    database.session.add(customer)
    database.session.commit()

    assert customer.id is not None
    assert customer.name == 'John Doe'
    assert customer.email == 'john.doe@email.org'

def test_create_customer_optional_phone(database):
    customer = Customer(
        name='John Doe',
        email='john.doe@email.org'
    )

    database.session.add(customer)
    database.session.commit()

    assert customer.id is not None
    assert customer.name == 'John Doe'