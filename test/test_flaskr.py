import json
import pytest
from app import app

planet = {
    'name': 'Saturn',
    'climate': 'cold',
    'terrain': 'gas'
}

@pytest.fixture
def reset_client():
    app.config['TESTING'] = True
    test_app = app.test_client()

    # get all planets and delete all
    response = test_app.get('/planets')
    for planet in response.json:
        test_app.delete('/planets/' + planet['_id']['$oid'])

    yield test_app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    test_app = app.test_client()
    yield test_app

def test_get_planets_type(reset_client):
    '''Asserts that GET /planets returns 200 and a JSON list.'''
    response = reset_client.get('/planets')
    assert response.status_code == 200
    assert response.json == []

def test_insert_planet(client):
    '''
    Asserts that a planet can be correctly inserted.
    '''
    headers = {'content-type': 'application/json'}
    response = client.put('/planets', data=json.dumps(planet), headers=headers)

    planet['_id'] = response.json['_id']
    planet['film_count'] = response.json['film_count']

    assert response.status_code == 201
    assert response.json == planet

def test_get_planet_by_id(client):
    '''
    Asserts that a planet can be correctly retrieved by its ID.
    '''
    response = client.get('/planets/' + planet['_id']['$oid'])
    assert response.status_code == 200
    assert response.json == planet

def test_get_planet_by_name(client):
    '''
    Asserts that a planet can be correctly retrieved by its name.
    '''
    response = client.get('/planets/name/' + planet['name'])
    assert response.status_code == 200
    assert response.json == planet

def test_delete_planet(client):
    '''
    Asserts that the previously inserted planet can be correctly removed.
    '''
    # delete the previously inserted planet
    headers = {'content-type': 'application/json'}
    response = client.delete('/planets/' + planet['_id']['$oid'],
                             headers=headers)
    assert response.status_code == 204
