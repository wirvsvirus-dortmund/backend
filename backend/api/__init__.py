from flask import (jsonify, Blueprint)
from flask_restful import Api, Resource

from ..models import Shop


api_bp = Blueprint('api_bp', __name__)
api = Api(api_bp)

def as_dict(instance):
    ''' Transform a model instance into a dict '''
    return {
        c.name: getattr(instance, c.name)
        for c in instance.__table__.columns
    }

class Shops(Resource):
    def get(self):
        all_saved_shops = [as_dict(shop) for shop in Shop.query.all()]
        return jsonify(status='success', shops=all_saved_shops)


api.add_resource(Shops, '/shops')
