import pytest
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from models.user import User
from models.password import UserPassword

def test_create_user(database):
    password = UserPassword(
        password_hash='newuserpass'
    )

    database.add(password)
    database.commit()

    user = User(
        username='newuser',
        email='newuser@email.com',
        password_id=password.id
    )

    database.add(user)
    database.commit()

    assert user.id is not None
    assert user.username == 'newuser'
    assert user.email == 'newuser@email.com'

def test_unique_username(database):
    password = UserPassword(
        password_hash='newuserpass'
    )

    database.add(password)
    database.commit()

    user1 = User(
        username='newuser',
        email='newuser@email.com',
        password_id=password.id
    )

    database.add(user1)
    database.commit()

    user2 = User(
        username='newuser',
        email='newuser2@email.com',
        password_id=password.id
    )

    database.add(user2)

    with pytest.raises(IntegrityError):
        database.commit()

def test_unique_email(database):
    password = UserPassword(
        password_hash='newuserpass'
    )

    database.add(password)
    database.commit()

    user1 = User(
        username='newuser',
        email='newuser@email.com',
        password_id=password.id
    )

    database.add(user1)
    database.commit()

    user2 = User(
        username='newuser2',
        email='newuser@email.com',
        password_id=password.id
    )

    database.add(user2)

    with pytest.raises(IntegrityError):
        database.commit()

def test_hashed_password(database):
    plain_password = 'newuserpass'

    password = UserPassword(
        password_hash=generate_password_hash('newuserpass')
    )

    database.add(password)
    database.commit()

    user = User(
        username='newuser',
        email='newuser@email.com',
        password_id=password.id
    )

    database.add(user)
    database.commit()

    assert user.password is not plain_password
    assert check_password_hash(user.password.password_hash, plain_password)
    assert not check_password_hash(user.password.password_hash, 'wrongpassword')

def test_query_user(database):
    user = database.query(User).first()

    assert user is not None
    assert user.id is not None
    assert user.username == 'testuser'
    assert user.email == 'test@email.com'