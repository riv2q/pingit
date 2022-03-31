"""Module for the `pingit` service."""
from flask import Flask
from flask_restful_swagger_3 import Api

app = Flask(__name__)
api = Api(app, version="1.0", title="PingIt")
