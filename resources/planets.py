import json
import requests
from bson import json_util
from bson.errors import InvalidId
from flask_restful import reqparse, Resource
import common.db as db


class Planets(Resource):
    '''Resource for getting planet list and insert new planets.'''
    def get(self):
        result = db.get_all()
        return json.loads(json_util.dumps(result))

    def put(self):
        # TODO check input validity (non-empty name)
        # TODO Request parsing will be discontinued from flask_restful. Change
        # it to another library which implements request parsing (e.g.:
        # Marshmallow).
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help='Name of the planet.')
        parser.add_argument('climate', type=str, required=True,
                            help='Climate of the planet.')
        parser.add_argument('terrain', type=str, required=True,
                            help='Terrain of the planet.')
        planet = parser.parse_args()

        # get films count
        try:
            response = requests.get("https://swapi.co/api/planets/",
                                    {"search": planet.name})
            if response.json()['count'] > 0:
                planet['film_count'] = \
                    len(response.json()['results'][0]['films'])
            else:
                planet['film_count'] = 0
        except json.decoder.JSONDecodeError:
            planet['film_count'] = 0

        # insert planet
        planet_id = db.insert_one(planet)

        # return planet with its newly-generated ID
        planet['_id'] = {'$oid': str(planet_id)}
        return planet, 201

class PlanetByID(Resource):
    '''Resource for getting and removing planet by ID.'''
    def get(self, planet_id):
        try:
            result = db.get_one_by_id(planet_id)
            if result is None:
                return {'message': 'Planet not found by ID.'}, 404
            return json.loads(json_util.dumps(result))
        except InvalidId as err:
            return {"message": str(err)}, 400

    def delete(self, planet_id):
        try:
            result = db.delete_one(planet_id)
            if result > 0:
                return {'message': 'Planet successfully deleted.'}, 204
            if result == 0:
                return {'message': 'Planet not found by ID.'}, 404
        except InvalidId as err:
            return {"message": str(err)}, 400

        return {'message': 'Unknown error.'}, 500

class PlanetByName(Resource):
    '''Resource for getting planet by name.'''
    def get(self, planet_name):
        planet = db.get_one_by_name(planet_name)
        if planet is None:
            return {'message': 'Planet not found by name.'}, 404
        return json.loads(json_util.dumps(planet))
