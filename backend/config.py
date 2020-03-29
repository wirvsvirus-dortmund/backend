import os
from datetime import timedelta

from dotenv import load_dotenv

from .json_encoder import JSONEncoder

load_dotenv()


def getenvbool(key, default=False):
    '''Get a boolean from an env variable.
    Case insensitive and matches `on`, `true`, `yes` as `True`,
    everything else as `False`
    '''
    value = os.getenv(key)
    if value is None:
        return default
    return value.lower() in {'on', 'true', 'yes'}


class Config:
    '''App configuration.

    Should get everything from environment variables to be dotenv and docker friendly.
    Provide suitable defaults if appropriate using `os.getenv(var, default)`.
    For required fields use `os.environ[var]`
    '''

    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # make deprecation warning go away
    SERVER_NAME = os.getenv('SERVER_NAME', 'localhost:8000')
    USE_HTTPS = getenvbool('SERVER_NAME')

    # secret key is needed for sessions and tokens
    SECRET_KEY = os.environ['SECRET_KEY']

    # use our own jsonencoder that can handle dates with flask_restful
    RESTFUL_JSON = {'cls': JSONEncoder}

    # how long a login cookie stays valid
    REMEMBER_COOKIE_DURATION = timedelta(days=10)

    # config for the email server so this app can send mails
    MAIL_SENDER = os.environ['MAIL_SENDER']
    MAIL_SERVER = os.environ['MAIL_SERVER']
    MAIL_USE_TLS = getenvbool('MAIL_USE_TLS')
    MAIL_USE_SSL = getenvbool('MAIL_USE_SSL')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    if MAIL_USERNAME is not None and MAIL_PASSWORD is None:
        raise KeyError('MAIL_PASSWORD is required when MAIL_USERNAME is set')
