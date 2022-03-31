"""Main pingit module."""
import json
import logging
import requests
import time

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


class Pingit(Ping):
    """Endpoint for pingit.

    Endpoint created just for fun. Goal was to show connection time
    and status code in few iterations in one request/response.
    Using multipart response.
    """

    def ping_service_generator(self):
        """Ganerate ping of the service response."""
        session = requests.Session()
        for round_number in range(10):
            start_time = time.time()
            response = session.get(self.url, verify=False)
            end_time = time.time()
            yield (
                "{url} status={status} iter={number} "
                "time={rtime:.3f} ms\r\n".format(
                    url=self.url,
                    status=response.status_code,
                    rtime=end_time - start_time,
                    number=round_number
                )
            )
            time.sleep(1)
        session.close()

    def post(self):
        """Handle 'GET' request."""
        return Response(
            self.ping_service_generator(),
            mimetype='multipart/x-mixed-replace'
        )


# Assaign endpoints to the application
api.add_resource(Home, '/')
api.add_resource(Ping, '/ping')
api.add_resource(Info, '/info')
api.add_resource(Pingit, '/pingit')

if __name__ == "__main__":
    app.run(debug=True)
