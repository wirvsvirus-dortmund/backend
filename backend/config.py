import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    '''App configuration.

    Should get everything from environment variables to be dotenv and docker friendly.
    Provide suitable defaults if appropriate using `os.getenv(var, default)`.
    For required fields use `os.environ[var]`
    '''

    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # make deprecation warning go away

    # secret key is needed for sessions and tokens
    SECRET_KEY = os.environ['SECRET_KEY']
