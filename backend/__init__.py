from flask import Flask
from flask_migrate import Migrate

from .config import Config
from .models import db
from .api import api

def create_app(config=Config):
    '''initialize the flask app'''
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(api.blueprint)

    return app
