from flask import Blueprint
from flask_restful import Api, Resource, abort, reqparse
import dateutil.parser

from ..models import db, Shop, CustomerDatapoint


api_bp = Blueprint('api_bp', __name__)
api = Api(api_bp)


def parse_date(s):
    return dateutil.parser.parse(s)


def all_as_dict(query):
    '''Return a list of dicts for all rows in query'''
    return [row.as_dict() for row in query]


def get_or_404(model, id_):
    '''return with 404 if there is no instance of a given model with id `id_`'''
    result = model.query.get(id_)
    if result is None:
        abort(404, message=f'{model.__name__} with id {id_} does not exist')
    else:
        return result


class ShopListAPI(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('name', required=True)
    parser.add_argument('address', required=True)
    parser.add_argument('capacity', type=int, required=True)
    parser.add_argument('contact_info', required=True)

    def get(self):
        return dict(status='success', shops=all_as_dict(Shop.query.all()))

    def post(self):
        '''Adds a new shop'''
        args = self.parser.parse_args()
        new_shop = Shop(**args)
        db.session.add(new_shop)
        db.session.commit()
        return dict(status='success', shop=new_shop.as_dict()), 201


class ShopAPI(Resource):
    def get(self, shop_id):
        return get_or_404(Shop, shop_id).as_dict()


class CustomersAPI(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('timestamp', type=parse_date, required=True)
    parser.add_argument('customers_inside', type=int, required=True)
    parser.add_argument('queue_size', type=int, required=True)

    def get(self, shop_id):
        get_or_404(Shop, shop_id)
        data = all_as_dict(CustomerDatapoint.query.filter_by(shop_id=shop_id))
        return dict(status='success', shop_id=shop_id, customers=data)

    def post(self, shop_id):
        '''adds a new data point to the customer timeseries'''
        get_or_404(Shop, shop_id)
        args = self.parser.parse_args()
        data = CustomerDatapoint(**args, shop_id=shop_id)
        db.session.add(data)
        db.session.commit()
        return dict(status='success', data=data.as_dict()), 201


api.add_resource(ShopListAPI, '/shops')
api.add_resource(ShopAPI, '/shops/<int:shop_id>')
api.add_resource(CustomersAPI, '/shops/<int:shop_id>/customers')
