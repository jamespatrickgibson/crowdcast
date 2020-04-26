from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api

from resources.healthcheck import HealthCheck
from resources.venue import Venue

app = Flask(__name__)
CORS(app)
api = Api(app)
api.add_resource(HealthCheck, '/')
api.add_resource(Venue, '/venues')

if __name__ == '__main__':
    app.run(debug=True)
