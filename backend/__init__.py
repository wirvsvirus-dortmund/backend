from flask import Flask
from flask_migrate import Migrate

from .config import Config
from .models import db
from .api import api
from .authentication import login, auth
from .json_encoder import JSONEncoder


def create_app(config=Config):
    '''initialize the flask app'''
    app = Flask(__name__)

    # parse config
    app.config.from_object(config)

    app.json_encoder = JSONEncoder

    # init flask extensions
    db.init_app(app)
    login.init_app(app)
    Migrate(app, db)

    # register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(api.blueprint, url_prefix='/api')

    return app
