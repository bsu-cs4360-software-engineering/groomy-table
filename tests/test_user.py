import pytest
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from models.user import User

def test_create_user(database):
    user = User(
        username='newuser',
        email='newuser@email.com',
        password='newuserpass'
    )

    database.session.add(user)
    database.session.commit()

    assert user.id is not None
    assert user.username == 'newuser'
    assert user.email == 'newuser@email.com'

def test_unique_username(database):
    user1 = User(
        username='newuser',
        email='newuser@email.com',
        password='newuserpass'
    )

    database.session.add(user1)
    database.session.commit()

    user2 = User(
        username='newuser',
        email='newuser2@email.com',
        password='newuserpass'
    )

    database.session.add(user2)

    with pytest.raises(IntegrityError):
        database.session.commit()

def test_unique_email(database):
    user1 = User(
        username='newuser',
        email='newuser@email.com',
        password='newuserpass'
    )

    database.session.add(user1)
    database.session.commit()

    user2 = User(
        username='newuser2',
        email='newuser@email.com',
        password='newuserpass'
    )

    database.session.add(user2)

    with pytest.raises(IntegrityError):
        database.session.commit()

def test_hashed_password(database):
    plain_password = 'newuserpass'

    user = User(
        username='newuser',
        email='newuser@email.com',
        password=generate_password_hash('newuserpass')
    )

    database.session.add(user)
    database.session.commit()

    assert user.password != plain_password
    assert check_password_hash(user.password, plain_password)
    assert not check_password_hash(user.password, 'wrongpassword')