from datetime import datetime, timedelta

def test_create_apppointment_success(client, csrf_token):
    today = datetime.today().date()
    fixed_date = today + timedelta(days=1)
    fixed_time = '09:00 AM'

    response = client.post('/appointments', data={
        'name': 'testuser',
        'email': 'test@user.com',
        'street_address': '0000 Avenue NE',
        'date': fixed_date,
        'time': fixed_time,
        'csrf_token': csrf_token
    })

    assert response.status_code == 302

def test_invalid_email(client, csrf_token):
    today = datetime.today().date()
    fixed_date = today + timedelta(days=1)
    fixed_time = '09:00 AM'

    response = client.post('/appointments', data={
        'name': 'testuser',
        'email': 'bademail',
        'street_address': '0000 Avenue NE',
        'date': fixed_date,
        'time': fixed_time,
        'csrf_token': csrf_token
    })

    assert response.status_code == 200

def test_phone_number(client, csrf_token):
    today = datetime.today().date()
    fixed_date = today + timedelta(days=1)
    fixed_time = '09:00 AM'

    response = client.post('/appointments', data={
        'name': 'testuser',
        'email': 'test@user.com',
        'phone_number': '123-456-7890',
        'street_address': '0000 Avenue NE',
        'date': fixed_date,
        'time': fixed_time,
        'csrf_token': csrf_token
    })

    assert response.status_code == 302

def test_empty_name(client, csrf_token):
    today = datetime.today().date()
    fixed_date = today + timedelta(days=1)
    fixed_time = '09:00 AM'

    response = client.post('/appointments', data={
        'name': '',
        'email': 'test@user.com',
        'street_address': '0000 Avenue NE',
        'date': fixed_date,
        'time': fixed_time,
        'csrf_token': csrf_token
    })

    assert response.status_code == 200

def test_empty_address(client, csrf_token):
    today = datetime.today().date()
    fixed_date = today + timedelta(days=1)
    fixed_time = '09:00 AM'

    response = client.post('/appointments', data={
        'name': 'testuser',
        'email': 'test@user.com',
        'street_address': '',
        'date': fixed_date,
        'time': fixed_time,
        'csrf_token': csrf_token
    })

    assert response.status_code == 200

def test_invalid_date(client, csrf_token):
    fixed_date = datetime.today().date()
    fixed_time = '09:00 AM'

    response = client.post('/appointments', data={
        'name': 'testuser',
        'email': 'test@user.com',
        'street_address': '',
        'date': fixed_date,
        'time': fixed_time,
        'csrf_token': csrf_token
    })

    assert response.status_code == 200