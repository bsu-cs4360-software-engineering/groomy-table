def test_get_index(client):
    response = client.get('/')
    assert b'<title>Groomy</title>' in response.data

def test_get_login(client):
    response = client.get('/login')
    assert b'Login' in response.data 

def test_get_dash_without_login(client):
    response = client.get('/dashboard')

    # Expect redirect to login
    assert response.status_code == 302
    assert b'Redirecting' in response.data