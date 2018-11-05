import json
import requests
from bson import json_util
from bson.errors import InvalidId
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from flask_restful import reqparse, Api, Resource


class Planets(Resource):
    '''Resource for getting planet list and insert new planets.'''
    def __init__(self, **kwargs):
        self.planets_collection = kwargs['collection']

    def get(self):
        result = self.planets_collection.find()
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
        planet_id = self.planets_collection.insert_one(planet).inserted_id

        # return planet with its newly-generated ID
        planet['_id'] = {'$oid': str(planet_id)}
        return planet, 201

class PlanetByID(Resource):
    '''Resource for getting and removing planet by ID.'''
    def __init__(self, **kwargs):
        self.planets_collection = kwargs['collection']

    def get(self, planet_id):
        planet = None
        try:
            # TODO set custom error message for 404
            planet = self.planets_collection.find_one_or_404({'_id': ObjectId(planet_id)})
        except InvalidId as err:
            return ({"message": str(err)}, 400)
        return json.loads(json_util.dumps(planet))

    def delete(self, planet_id):
        try:
            result = self.planets_collection.delete_one({'_id': ObjectId(planet_id)})
            if result.acknowledged is True:
                if result.deleted_count > 0:
                    return {'message': 'Planet successfully deleted.'}, 204
                else:
                    return {'message': 'Planet not found by ID.'}, 404
        except InvalidId as err:
            return ({"message": str(err)}, 400)

        return {'message': 'Unknown error.'}, 500

class PlanetByName(Resource):
    '''Resource for getting planet by name.'''
    def __init__(self, **kwargs):
        self.planets_collection = kwargs['collection']

    def get(self, planet_name):
        # TODO set custom error message for 404
        planet = self.planets_collection.find_one_or_404({'name': planet_name})
        return json.loads(json_util.dumps(planet))
