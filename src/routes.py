from flask import Blueprint
from flask_restful import Api


bp_example = Blueprint('example', __name__, url_prefix='/api/example')
api_example = Api(bp_example)
