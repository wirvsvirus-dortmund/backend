import pytest
import tempfile


@pytest.fixture(scope='session')
def app():
    from backend import Config, create_app
    with tempfile.NamedTemporaryFile(suffix='.sqlite', prefix='db_testing') as f:

        class TestingConfig(Config):
            SQLALCHEMY_DATABASE_URI = 'sqlite:///' + f.name

        app = create_app(TestingConfig())

        yield app


@pytest.fixture(scope='session')
def client(app):
    from backend.models import db

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
