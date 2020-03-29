from flask import Blueprint
from flask_restful import Api

from .shops import ShopListAPI, ShopAPI, ShopDataAPI
from .users import UsersAPI


api_bp = Blueprint('api_bp', __name__)
api = Api(api_bp)


api.add_resource(ShopListAPI, '/shops')
api.add_resource(ShopAPI, '/shops/<int:shop_id>')
api.add_resource(ShopDataAPI, '/shops/<int:shop_id>/data')
api.add_resource(UsersAPI, '/users')
