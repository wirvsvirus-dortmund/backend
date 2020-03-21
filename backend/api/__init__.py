from flask import Blueprint
from flask_restful import Api, Resource, abort, reqparse
import dateutil.parser

from ..models import db, Shop, CustomerDatapoint


api_bp = Blueprint('api_bp', __name__)
api = Api(api_bp)


def parse_date(s):
    return dateutil.parser.parse(s)


def as_dict(instance):
    ''' Transform a model instance into a dict '''
    return {
        c.name: getattr(instance, c.name)
        for c in instance.__table__.columns
    }


def all_as_dict(query):
    '''Return a list of dicts for all rows in query'''
    return [as_dict(row) for row in query]


def abort_if_not_exists(model, id_):
    '''return with 404 if there is no instance of a given model with id `id_`'''
    if model.query.get(id_) is None:
        abort(404, message=f'{model.__name__} with id {id_} does not exist')


class Shops(Resource):
    def get(self):
        return dict(status='success', shops=all_as_dict(Shop.query.all()))


class Customers(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('timestamp', type=parse_date, required=True)
    parser.add_argument('customers_inside', type=int, required=True)
    parser.add_argument('queue_size', type=int, required=True)

    def get(self, shop_id):
        abort_if_not_exists(Shop, shop_id)
        data = all_as_dict(CustomerDatapoint.query.filter_by(shop_id=shop_id))
        return dict(status='success', shop_id=shop_id, customers=data)

    def post(self, shop_id):
        abort_if_not_exists(Shop, shop_id)
        args = self.parser.parse_args()
        data = CustomerDatapoint(**args, shop_id=shop_id)
        db.session.add(data)
        db.session.commit()
        return dict(status='success', data=as_dict(data)), 201


api.add_resource(Shops, '/shops')
api.add_resource(Customers, '/shops/<int:shop_id>/customers')
