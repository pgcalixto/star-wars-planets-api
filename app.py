import json
from bson import json_util
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

api.add_resource(Planets, '/')

if __name__ == '__main__':
    app.run(debug=True)
