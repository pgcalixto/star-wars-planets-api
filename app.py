from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

planets = []

class Planets(Resource):
    def get(self):
        return planets

api.add_resource(Planets, '/')

if __name__ == '__main__':
    app.run(debug=True)
