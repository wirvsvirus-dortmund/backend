from flask import Blueprint
from flask_restful import Api

from .shops import ShopListAPI, ShopAPI, DataAPI


api_bp = Blueprint('api_bp', __name__)
api = Api(api_bp)


api.add_resource(ShopListAPI, '/shops')
api.add_resource(ShopAPI, '/shops/<int:shop_id>')
api.add_resource(DataAPI, '/shops/<int:shop_id>/data')
