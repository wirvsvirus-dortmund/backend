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
        if all_saved_shops:
            return jsonify(all_saved_shops)
        else:
            return "Currently we haven't stored any shops in our database."

api.add_resource(Shops, '/shops')
