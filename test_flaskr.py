import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    test_app = app.test_client()
    yield test_app

def test_get_planets_type(client):
    '''Asserts that GET /planets returns 200 and a JSON list.'''
    response = client.get('/planets')
    assert response.status_code == 200
    assert type(response.json) == list
