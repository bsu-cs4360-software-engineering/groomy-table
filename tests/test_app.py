import pytest

class TestApp():

    def test_get_index(self, client):
        response = client.get('/')
        assert b'<title>Groomy</title>' in response.data

    def test_get_login(self, client):
        response = client.get('/login')
        assert b'Login' in response.data 

class TestLogin():
    def test_login_success(self, client, csrf_token):
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword',
            'csrf_token': csrf_token
        })

        # Redirect to dashboard
        assert response.status_code == 302

    def test_login_failure(self, client, csrf_token):
        response = client.post('/login', data={
            'username': 'wronguser',
            'password': 'wrongpass',
            'csrf_token': csrf_token
        })

        # Failed login stays on same page
        assert response.status_code == 200
        assert b'Invalid username or password.' in response.data

    def test_logout(self, client, csrf_token):
        # Login
        client.post('/login', data={
            'username': 'wronguser',
            'password': 'wrongpass',
            'csrf_token': csrf_token
        })

        response = client.get('/logout')
        
        # Redirect to login
        assert response.status_code == 302