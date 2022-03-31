"""Main pingit module."""
import json
import logging
import requests
import time

import validators
from flask import Flask, request, Response
from flask_restful import reqparse, abort
from flask_restful_swagger_3 import (
    Api, Resource, swagger, get_swagger_blueprint)


app = Flask(__name__)
api = Api(app, version="1.0", title="PingIt")


log = logging.getLogger("pingit")


@swagger.tags("Endpoints")
class Info(Resource):
    """Endpoint for info."""

    @swagger.response(
        response_code=200,
        description="Returns simple static json",
        no_content=True
    )
    @swagger.response(
        response_code=304,
        description="The page hasn't changed (ETag unchanged)",
        no_content=True,
    )
    @swagger.response(
        response_code=412,
        description=(
            "Etag provided in the If-Match header does not match the "
            "current ETag"
        ),
        no_content=True,
    )
    @swagger.parameter(
        _in="header",
        name="If-None-Match",
        description="Etag If-None-Match header",
        schema={"type": "string"},
        required=False,
    )
    @swagger.parameter(
        _in="header",
        name="If-Match",
        description="Etag If-Match header",
        schema={"type": "string"},
        required=False,
    )
    def get(self):
        """Handle 'GET' request."""
        message = json.dumps({"Receiver": "Cisco is the best!"})
        response = Response(response=message, status=200,
                            mimetype="application/json")
        response.add_etag()
        return response.make_conditional(request)


@swagger.tags("Endpoints")
class Ping(Resource):
    """Endpoint for ping."""

    post_parser = reqparse.RequestParser()
    post_parser.add_argument(
        "url",
        type=str,
        required=True,
        help="parameter has not been specified",
    )

    def __init__(self):
        """Initialize request parser with proper arguments."""
        # Collect arguments
        arguments = self.post_parser.parse_args()

        # Assaign arguments
        self.url = arguments["url"]

        # Validate site argument
        if validators.url(self.url) is not True:
            error_msg = "url parameter is not valid, provide http/https url"
            log.error(error_msg)
            abort(400, error=error_msg)
        super(Ping, self).__init__()

    @swagger.reqparser(name="url_parameter_ping", parser=post_parser)
    @swagger.response(
        description="Returns simple static json",
        response_code=200,
        no_content=True
    )
    @swagger.response(
        response_code=400, description="Bad Request", no_content=True
    )
    def post(self):
        """Handle 'POST' request."""
        response = requests.get(self.url, verify=False)
        return Response(response=response, status=200, mimetype="text/html")


@swagger.tags("Bonus - stream response example, use with curl")
class Pingit(Ping):
    """Endpoint for pingit.

    Endpoint created just for fun. Goal was to show connection time
    and status code in few iterations in one request/response.
    Using multipart response.
    """

    post_parser = reqparse.RequestParser()
    post_parser.add_argument(
        "url", type=str, required=True, help="parameter has not been specified"
    )

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
                    number=round_number,
                )
            )
            time.sleep(1)
        session.close()

    @swagger.reqparser(name="url_parameter_pingit", parser=post_parser)
    @swagger.response(
        description="Returns simple static json",
        response_code=200,
        no_content=True
    )
    @swagger.response(
        response_code=400,
        description="Bad Request",
        no_content=True
    )
    def post(self):
        """Handle 'GET' request."""
        return Response(
            self.ping_service_generator(), mimetype="multipart/x-mixed-replace"
        )


# Assaign endpoints to the application
api.add_resource(Ping, "/ping")
api.add_resource(Info, "/info")
api.add_resource(Pingit, "/pingit")


SWAGGER_URL = "/doc"  # URL for exposing Swagger UI (without trailing '/')
API_URL = "endpoints.json"  # Our API url (can of course be a local resource)

swagger_blueprint = get_swagger_blueprint(
    api.open_api_object, swagger_prefix_url=SWAGGER_URL, swagger_url=API_URL
)
app.register_blueprint(swagger_blueprint)


if __name__ == "__main__":
    app.run(debug=True)
