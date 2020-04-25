from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api

app = Flask(__name__)
CORS(app)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
