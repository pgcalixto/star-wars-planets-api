import json
import requests
from flask import Flask
from flask_pymongo import PyMongo
from flask_restful import Api
from resources.planets import Planets, PlanetByID, PlanetByName

app = Flask(__name__)
api = Api(app)
api.add_resource(Planets, '/planets')
api.add_resource(PlanetByID, '/planets/<string:planet_id>')
api.add_resource(PlanetByName, '/planets/name/<string:planet_name>')

if __name__ == '__main__':
    app.run(debug=True)
