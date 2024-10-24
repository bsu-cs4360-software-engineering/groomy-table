def test_create_account_success(client, csrf_token):
    response = client.post('/create_account', data={
        'username': 'testuser2',
        'email': 'test@user.com',
        'password': 'testpass',
        'confirm_password': 'testpass',
        'csrf_token': csrf_token
    })

    assert response.status_code == 302
    assert b'Login'

def test_invalid_email(client, csrf_token):
    response = client.post('/create_account', data={
        'username': 'testuser2',
        'email': 'bademail',
        'password': 'testpass',
        'confirm_password': 'testpass',
        'csrf_token': csrf_token
    })

    assert response.status_code == 200
    assert b'Invalid email address.'

def test_nonmatching_passwords(client, csrf_token):
    response = client.post('/create_account', data={
        'username': 'testuser2',
        'email': 'test@user.com',
        'password': 'testpass',
        'password': 'badpass',
        'csrf_token': csrf_token
    })

    assert response.status_code == 200
    assert b'Passwords do not match.'

def test_user_already_exists(client, csrf_token):
    response = client.post('/create_account', data={
        'username': 'testuser',
        'email': 'test@user.com',
        'password': 'testpass',
        'password': 'testpass',
        'csrf_token': csrf_token
    })

    assert response.status_code == 200
    assert b'Username taken.'