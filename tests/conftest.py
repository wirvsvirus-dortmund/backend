import pytest
import tempfile
from backend import Config


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'

    # Bcrypt algorithm hashing rounds (reduced for testing purposes only!)
    BCRYPT_LOG_ROUNDS = 4

    # Enable the TESTING flag to disable the error catching during request handling
    # so that you get better error reports when performing test requests
    TESTING = True

    # Disable CSRF tokens in the Forms (only valid for testing purposes!)
    WTF_CSRF_ENABLED = False

    # don't really send out mails during unit tests
    MAIL_SUPPRESS_SEND = True
    MAIL_SENDER = 'Supermarkt <supermarkt@test.org>'


@pytest.fixture(scope='session')
def app():
    from backend import create_app

    with tempfile.NamedTemporaryFile(suffix='.sqlite', prefix='db_testing') as f:

        TestingConfig.SQLALCHEMY_DATABASE_URI += f.name
        app = create_app(TestingConfig)

        yield app


@pytest.fixture(scope='session')
def client(app):
    from backend.models import db

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
