class TestApp():
    def test_get_index(self, client):
        response = client.get('/')
        assert b'<title>Groomy</title>' in response.data

    def test_get_login(self, client):
        response = client.get('/login')
        assert b'Login' in response.data 