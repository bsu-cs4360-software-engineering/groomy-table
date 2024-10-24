def test_login_success(client, csrf_token):
    response = client.post('/login', data={
        'username_or_email': 'testuser',
        'password': 'testpassword',
        'csrf_token': csrf_token
    })

    # Redirect to dashboard
    assert response.status_code == 302
    assert b'<title>Dashboard - Groomy</title>'

def test_login_with_email(client, csrf_token):
    response = client.post('/login', data={
        'username_or_email': 'test@email.com',
        'password': 'testpassword',
        'csrf_token': csrf_token
    })

    assert response.status_code == 302

def test_login_failure(client, csrf_token):
    response = client.post('/login', data={
        'username_or_email': 'wronguser',
        'password': 'wrongpass',
        'csrf_token': csrf_token
    })

    # Failed login stays on same page
    assert response.status_code == 200
    assert b'Invalid username or password.' in response.data

def test_logout(client, csrf_token):
    # Login
    client.post('/login', data={
        'username_or_email': 'wronguser',
        'password': 'wrongpass',
        'csrf_token': csrf_token
    })

    response = client.get('/logout')
    
    # Redirect to login
    assert response.status_code == 302
    assert b'Login'