import json
import pytest
from app import app

planet = {
    'name': 'Saturn',
    'climate': 'cold',
    'terrain': 'gas'
}

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

def test_empty_all_planets(client):
    '''
    Asserts that all planets can be removed and GET /planets returns 200 and
    an empty JSON list.
    '''
    # get all planets
    response = client.get('/planets')

    # delete all planets
    for planet in response.json:
        client.delete('/planets/' + planet['_id']['$oid'])

    response = client.get('/planets')
    assert response.status_code == 200
    assert response.json == []

def test_insert_planet(client):
    '''
    Asserts that a planet can be correctly inserted.
    '''
    headers = {'content-type': 'application/json'}
    response = client.put('/planets', data=json.dumps(planet), headers=headers)

    assert response.status_code == 201
    assert planet['name'] == response.json['name']
    assert planet['climate'] == response.json['climate']
    assert planet['terrain'] == response.json['terrain']

    pytest.planet_id = response.json['_id']['$oid']
