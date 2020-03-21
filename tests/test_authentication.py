import pytest


PASSWORD = 'very-good-password'


@pytest.fixture(scope='module')
def user(client):
    from backend.models import User, db

    u = User(
        username='test',
        email='test@example.org',
    )
    u.set_password(PASSWORD)
    db.session.add(u)
    db.session.commit()

    return u


def test_check_password(user):
    assert not user.check_password('foo')
    assert user.check_password(PASSWORD)


def test_login_logout(client, user):
    ret = client.post(
        '/login/',
        data={'username': user.username, 'password': PASSWORD}
    )
    assert ret.status_code == 200
    assert ret.json['status'] == 'success'
    assert ret.json['message'] == 'user logged in'

    ret = client.post('/logout/')
    assert ret.status_code == 200
    assert ret.json['status'] == 'success'
    assert ret.json['message'] == 'user logged out'

    ret = client.post(
        '/login/',
        data={'username': user.username, 'password': 'foo'}
    )
    assert ret.status_code == 401
    assert ret.json['status'] == 'error'
    assert ret.json['message'] == 'invalid user or password'


def test_login_required(app, client, user):
    from flask import Blueprint, jsonify
    from flask_login import login_required

    bp = Blueprint('test', 'test')

    @bp.route('/test_login_required/')
    @login_required
    def test():
        return jsonify({'status': 'success'})

    app.register_blueprint(bp)

    ret = client.get('/test_login_required/')
    assert ret.status_code == 401
    assert ret.json['status'] == 'access_denied'

    client.post('/login/', data={'username': user.username, 'password': PASSWORD})

    ret = client.get('/test_login_required/')
    assert ret.status_code == 200
    assert ret.json['status'] == 'success'
