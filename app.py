import json
import swapi
from bson import json_util
from bson.errors import InvalidId
from bson.objectid import ObjectId
from flask import Flask
from flask_pymongo import PyMongo
from flask_restful import reqparse, Api, Resource

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/starwars"

api = Api(app)
mongo = PyMongo(app)
planets_col = mongo.db["planets"]

def getFilmsByPlanet():
    '''Get number of Star Wars films by planet from SWAPI.

    Query the Star Wars API (SWAPI) for the planets' information and returns a
    list of Star Wars films number by planet.

    Returns:
        dict: Dictionary with planet name as key and film appearance count as
              value.
    '''
    return {p.name: len(p.films) for p in swapi.get_all("planets").iter()}

# Before starting the Flask API, store all films count by planets, from SWAPI.
FILM_COUNT_BY_PLANET = getFilmsByPlanet()

# TODO Request parsing will be discontinued from flask_restful. Change it to
# another library which implements request parsing (e.g.: Marshmallow).
parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name of the planet.')
parser.add_argument('climate', type=str, required=True,
                    help='Climate of the planet.')
parser.add_argument('terrain', type=str, required=True,
                    help='Terrain of the planet.')

class Planets(Resource):
    '''Resource for getting planet list and insert new planets.'''
    def get(self):
        planets = planets_col.find()
        return json.loads(json_util.dumps(planets))

    def put(self):
        # TODO check input validity (non-empty name)
        # insert planet
        planet = parser.parse_args()
        planet['films'] = 0
        if planet['name'] in FILM_COUNT_BY_PLANET:
            planet['films'] = FILM_COUNT_BY_PLANET[planet['name']]
        planet_id = planets_col.insert_one(planet).inserted_id

        # return planet with its generated ID
        planet['_id'] = {'$oid': str(planet_id)}
        return planet, 201

class PlanetByID(Resource):
    '''Resource for getting and removing planet by ID.'''
    def get(self, planet_id):
        planet = None
        try:
            # TODO set custom error message for 404
            planet = planets_col.find_one_or_404({'_id': ObjectId(planet_id)})
        except InvalidId as err:
            return ({"message": str(err)}, 400)
        return json.loads(json_util.dumps(planet))

    def delete(self, planet_id):
        try:
            result = planets_col.delete_one({'_id': ObjectId(planet_id)})
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
    def get(self, planet_name):
        # TODO set custom error message for 404
        planet = planets_col.find_one_or_404({'name': planet_name})
        return json.loads(json_util.dumps(planet))

api.add_resource(Planets, '/planets')
api.add_resource(PlanetByID, '/planets/<string:planet_id>')
api.add_resource(PlanetByName, '/planets/name/<string:planet_name>')

if __name__ == '__main__':
    app.run(debug=True)
