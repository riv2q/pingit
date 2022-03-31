"""Main pingit module."""
import json
import logging

from flask import Flask, Response, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

log = logging.getLogger('pingit')


class Home(Resource):

    def get(self):
        message = json.dumps({'message': 'Hello there!'})
        response = Response(
            response=message,
            status=200,
            mimetype="application/json"
        )
        response.add_etag()
        return response.make_conditional(request)


api.add_resource(Home, '/')

if __name__ == "__main__":
    app.run(debug=True)
