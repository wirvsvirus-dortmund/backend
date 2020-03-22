from flask import Flask
from flask_migrate import Migrate

from .config import Config
from .api import api
from .authentication import login, auth
from .json_encoder import JSONEncoder
from .mail import mail
from .models import db


def create_app(config=Config):
    '''initialize the flask app'''
    app = Flask(__name__)

    # parse config
    app.config.from_object(config)

    app.json_encoder = JSONEncoder

    # init flask extensions
    db.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    Migrate(app, db)

    # register blueprints
    app.register_blueprint(auth, url_prefix='/api')
    app.register_blueprint(api.blueprint, url_prefix='/api')

    return app
