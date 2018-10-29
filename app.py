import json
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

# TODO Request parsing will be discontinued from flask_restful. Change it to
# another library which implements request parsing (e.g.: Marshmallow).
parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name of the planet')
parser.add_argument('climate', required=True)
parser.add_argument('terrain', required=True)

class Planets(Resource):
    def get(self):
        planets = planets_col.find()
        return json.loads(json_util.dumps(planets))

    def put(self):
        # insert planet
        planet = parser.parse_args()
        planet_id = planets_col.insert_one(planet).inserted_id
        print(planet_id)

        # return list of planets
        planets = planets_col.find()
        return json.loads(json_util.dumps(planets))

class Planet(Resource):
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
    def get(self, planet_name):
        # TODO set custom error message for 404
        planet = planets_col.find_one_or_404({'name': planet_name})
        return json.loads(json_util.dumps(planet))

api.add_resource(Planets, '/')
api.add_resource(Planet, '/<string:planet_id>')
api.add_resource(PlanetByName, '/name/<string:planet_name>')

if __name__ == '__main__':
    app.run(debug=True)
