from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api

import peopleCountDaemon


app = Flask(__name__)
CORS(app)
api = Api(app)

daemon = peopleCountDaemon.PeopleCountDaemonObject()


class Occupancy(Resource):
    def get(self):
        return {
            'current_occupancy': daemon.get_current_occupancy(),
        }


api.add_resource(Occupancy, '/')

if __name__ == '__main__':
    daemon.start()
    app.run(debug=True)
