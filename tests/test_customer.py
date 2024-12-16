from models.customer import Customer

def test_create_customer(database):
    customer = Customer(
        name='John Doe',
        email='john.doe@email.org',
        phone_number='123-456-7890'
    )

    database.add(customer)
    database.commit()

    assert customer.id is not None
    assert customer.name == 'John Doe'
    assert customer.email == 'john.doe@email.org'

def test_create_customer_optional_phone(database):
    customer = Customer(
        name='John Doe',
        email='john.doe@email.org'
    )

    database.add(customer)
    database.commit()

    assert customer.id is not None
    assert customer.name == 'John Doe'
    assert customer.phone_number is None

def test_query_existing_customer(database):
    customer = database.query(Customer).first()

    assert customer is not None
    assert customer.name == 'John Doe'
    assert customer.email == 'john.doe@email.com'