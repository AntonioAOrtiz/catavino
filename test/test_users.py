import pytest
from app import create_app
from werkzeug.datastructures import Headers


@pytest.fixture
def client():
    app = create_app('config_tests.py')

    with app.test_client() as client:
        yield client


def test_prueba(client):
    rv = client.get('/')
    assert "Here is the" in rv.get_data(as_text=True)


def test_login(client):
    rv = client.post('/login', json={'username': 'selena', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/jugador', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert len(rsp) == 4
    assert "selena" in [d.get("username") for d in rsp]