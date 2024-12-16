import pytest
from werkzeug.security import generate_password_hash

from app_factory import create_app
from login_manager import login_manager
from database import db

from models.user import User
from models.password import UserPass
from models.customer import Customer

@pytest.fixture()
def app():
    app = create_app('sqlite://')

    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

        passwrd = UserPass(
            password_hash=generate_password_hash('testpassword')
        )

        db.add(passwrd)
        db.commit()

        test_user = User(
            username='testuser',
            email='test@email.com',
            password_id=passwrd.id
        )

        db.add(test_user)

        test_customer = Customer(
            name='John Doe',
            email='john.doe@email.com'
        )

        db.add(test_customer)
        db.commit()

    yield app

@pytest.fixture()
def database(app):
    with app.app_context():
        yield db

@pytest.fixture()
def client(app):
    return app.test_client()

def _extract_csrf(response):
    csrf_token = None
    for line in response.data.decode().splitlines():
        if 'name="csrf_token"' in line:
            start = line.find('value="') + len('value="')
            end = line.find('"', start)
            csrf_token = line[start:end]
            break

    return csrf_token

@pytest.fixture()
def csrf_token(client):
    response = client.get('/login')
    return _extract_csrf(response)