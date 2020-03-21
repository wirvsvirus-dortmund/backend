from flask import Flask
from flask_migrate import Migrate

from .config import Config
from .models import db


def create_app(config=Config):
    '''initialize the flask app'''
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    Migrate(app, db)

    return app
