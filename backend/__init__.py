from flask import Flask

from .config import Config
from .models import db


def create_app():
    '''initialize the flask app'''
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    return app
