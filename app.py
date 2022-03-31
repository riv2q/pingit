"""Main pingit module."""
import json
import logging
import requests

import validators
from flask import Flask, Response, request
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)

log = logging.getLogger('pingit')


class Home(Resource):
    """Endpoint /"""

    def get(self):
        """Handle 'GET' request."""
        message = json.dumps({'Message': 'Hello there!'})
        response = Response(
            response=message,
            status=200,
            mimetype="application/json"
        )
        response.add_etag()
        return response.make_conditional(request)


class Ping(Resource):
    """Endpoint for ping."""

    def __init__(self):
        """Initialize request parser with proper arguments."""
        # Describe arguments
        request_parser = reqparse.RequestParser()
        request_parser.add_argument(
            'url',
            type=str,
            required=True,
            help="parameter has not been specified"
        )

        # Collect arguments
        arguments = request_parser.parse_args()

        # Assaign arguments
        self.url = arguments['url']

        # Validate site argument
        if validators.url(self.url) is not True:
            error_msg = "site parameter is not valid"
            log.error(error_msg)
            abort(400, error=error_msg)
        super(Ping, self).__init__()

    def post(self):
        """Handle 'POST' request."""
        response = requests.get(self.url, verify=False)
        response = Response(
            response=response,
            status=200,
            mimetype="text/html"
        )
        response.add_etag()
        return response.make_conditional(request)


class Info(Resource):
    """Endpoint for info."""

    def get(self):
        """Handle 'GET' request."""
        message = json.dumps({'Receiver': 'Cisco is the best!'})
        response = Response(
            response=message,
            status=200,
            mimetype="application/json"
        )
        response.add_etag()
        return response.make_conditional(request)


# Assaign endpoints to the application
api.add_resource(Home, '/')
api.add_resource(Ping, '/ping')
api.add_resource(Info, '/info')

if __name__ == "__main__":
    app.run(debug=True)
