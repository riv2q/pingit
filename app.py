"""Main pingit module."""

import logging

from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

log = logging.getLogger('pingit')


class Home(Resource):

    def get(self):
        return {'message': 'Hello there!'}


api.add_resource(Home, '/')

if __name__ == "__main__":
    app.run(debug=True)
