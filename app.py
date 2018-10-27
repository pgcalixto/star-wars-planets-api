from flask import Flask
from flask_restful import reqparse, Api, Resource

app = Flask(__name__)
api = Api(app)

planets = []

# TODO Request parsing will be discontinued from flask_restful. Change it to
# another library which implements request parsing (e.g.: Marshmallow).
parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name of the planet')
parser.add_argument('climate', required=True)
parser.add_argument('terrain', required=True)

class Planets(Resource):
    def get(self):
        return planets

    def put(self):
        planet = parser.parse_args()
        planets.append(planet)
        return planets

api.add_resource(Planets, '/')

if __name__ == '__main__':
    app.run(debug=True)
