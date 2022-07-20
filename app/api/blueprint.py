from flask import Blueprint
from flask_restful import Api
from .controllers import RequestGetArhive, RequestGetFutureCity


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(RequestGetFutureCity, '/weather/future/<string:city_n>')
api.add_resource(RequestGetArhive, '/weather/archive/')
