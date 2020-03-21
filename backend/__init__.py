from flask import Flask
from flask_migrate import Migrate

from .config import Config
from .models import db
from .authentication import login, auth


def create_app(config=Config):
    '''initialize the flask app'''
    app = Flask(__name__)

    # parse config
    app.config.from_object(config)

    # init flask extensions
    db.init_app(app)
    login.init_app(app)
    Migrate(app, db)

    # register blueprints
    app.register_blueprint(auth)

    return app
