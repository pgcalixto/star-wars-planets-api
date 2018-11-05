import json
import requests
from flask import Flask
from flask_pymongo import PyMongo
from flask_restful import Api
from resources.planets import Planets, PlanetByID, PlanetByName

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/starwars"
mongo = PyMongo(app)

api = Api(app)
api.add_resource(Planets, '/planets',
                 resource_class_kwargs={'collection': mongo.db["planets"]})
api.add_resource(PlanetByID, '/planets/<string:planet_id>',
                 resource_class_kwargs={'collection': mongo.db["planets"]})
api.add_resource(PlanetByName, '/planets/name/<string:planet_name>',
                 resource_class_kwargs={'collection': mongo.db["planets"]})

if __name__ == '__main__':
    app.run(debug=True)
