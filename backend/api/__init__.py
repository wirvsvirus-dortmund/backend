from flask import (jsonify, request, render_template, Blueprint)
from flask_restful import Api, Resource, url_for

api_bp = Blueprint('api_bp', __name__)
api = Api(api_bp)


shops = dict()
class Shops(Resource):
    def get(self):
        return "Hello World"

api.add_resource(Shops, '/shops')
