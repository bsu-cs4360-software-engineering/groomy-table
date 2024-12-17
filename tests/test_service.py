import pytest
from sqlalchemy.exc import StatementError
from models.service import Service

def test_create_service(database):
    service = Service(
        name="Test Service",
        price=1.00
    )

    database.add(service)
    database.commit()

    assert service.id is not None
    assert service.name == 'Test Service'
    assert service.description is None
    assert service.price == 1.00

def test_non_main_service(database):
    service = Service(
        name="Addon Service",
        description="This is an addon package.",
        price=1.00,
        is_addon=True
    )

    database.add(service)
    database.commit()

    assert service.id is not None
    assert service.description == "This is an addon package."
    assert service.is_addon == True


def test_truncate_price(database):
    service = Service(
        name="Test Service",
        price=1.001,
    )

    database.add(service)
    database.commit()

    assert service.id is not None
    assert service.price == 1.00

def test_non_numeric_price(database):
    service = Service(
        name="Test Service",
        price="abc",
    )

    database.add(service)

    with pytest.raises(StatementError):
        database.commit()

def test_soft_delete_service(database):
    service = Service(
        name="Test Service",
        price=1.00
    )

    database.add(service)
    database.commit()

    service.deleted = True

    database.commit()

    service_query = database.query(Service).first()

    assert service_query is not None
    assert service_query.id is not None
    assert service_query.deleted is True