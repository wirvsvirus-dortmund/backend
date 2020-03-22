import pytest


PASSWORD = 'very-good-password'
USERNAME = 'test'
LOGIN_DATA = {'username': USERNAME, 'password': PASSWORD}


@pytest.fixture(scope='module')
def user(client):
    from backend.models import User, db

    u = User(
        username=USERNAME,
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
    ret = client.post('/api/login/', data=LOGIN_DATA)

    assert ret.status_code == 200
    assert ret.json['status'] == 'success'
    assert ret.json['message'] == 'user logged in'

    ret = client.post('/api/logout/')
    assert ret.status_code == 200
    assert ret.json['status'] == 'success'
    assert ret.json['message'] == 'user logged out'

    ret = client.post(
        '/api/login/',
        data={'username': user.username, 'password': 'foo'}
    )
    assert ret.status_code == 401
    assert ret.json['status'] == 'error'
    assert ret.json['message'] == 'invalid user or password'


def test_login_required(app, client, user):
    from flask import Blueprint, jsonify
    from flask_login import login_required

    # we create a small blueprint here that requires a login
    # so we can test the login_required function works correctly
    bp = Blueprint('test', 'test')

    @bp.route('/test_login_required/')
    @login_required
    def test():
        return jsonify({'status': 'success'})

    app.register_blueprint(bp)

    ret = client.get('/test_login_required/')
    assert ret.status_code == 401

    client.post('/api/login/', data=LOGIN_DATA)

    ret = client.get('/test_login_required/')
    assert ret.status_code == 200
    assert ret.json['status'] == 'success'


def test_roles(app, client, user):
    # we create a small blueprint here that requires a login
    # so we can test the login_required function works correctly
    from flask import Blueprint, jsonify
    from backend.authentication import role_required
    from backend.models import Role, db

    bp = Blueprint('test_roles', 'test_roles')

    @bp.route('/test_role_required/')
    @role_required('test_role')
    def test():
        return jsonify({'status': 'success'})

    app.register_blueprint(bp)

    r = client.post('/api/login/', data=LOGIN_DATA)
    assert r.status_code == 200

    # test request fails when user does not have needed role
    r = client.get('/test_role_required/')
    assert r.status_code == 401
    assert r.json['message'] == 'user lacks required role "test_role"'

    # test user can request the endpoint no that he/she has the role
    role = Role(name='test_role')
    user.roles.append(role)
    db.session.add(user, role)
    db.session.commit()

    assert user.has_role('test_role')
    assert not user.has_role('other_role')

    r = client.get('/test_role_required/')
    assert r.status_code == 200
    assert r.json['status'] == 'success'
