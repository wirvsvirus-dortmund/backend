import pytest


PASSWORD = 'very-good-password'
EMAIL = 'richard@feynman.org'
LOGIN_DATA = {'email': EMAIL, 'password': PASSWORD}


@pytest.fixture(scope='module')
def user(client):
    from backend.models import User, db, Role

    admin = Role(name='admin')
    u = User(
        name='Richard Feynman',
        email=EMAIL,
        roles=[admin],
    )
    u.set_password(PASSWORD)
    db.session.add(u, admin)
    db.session.commit()

    return u


def test_user_as_dict(user):
    d = user.as_dict()
    assert d == {
        'id': 1,
        'name': 'Richard Feynman',
        'email': EMAIL,
        'email_confirmed': False,
        'roles': ['admin'],
    }


def test_user_repr(user):
    assert repr(user) == f'<User 1: {EMAIL}>'


def test_check_password(user):
    assert not user.check_password('foo')
    assert user.check_password(PASSWORD)


def test_login_logout(client, user):
    from backend.models import db
    # unconfirmed email
    ret = client.post('/api/login/', data=LOGIN_DATA)
    assert ret.status_code == 401
    assert ret.json['message'] == 'unconfirmed_email'

    user.email_confirmed = True
    db.session.add(user)
    db.session.commit()

    # now it should work
    ret = client.post('/api/login/', data=LOGIN_DATA)
    assert ret.status_code == 200
    assert ret.json['message'] == 'user_logged_in'
    # only the session cookie should be there if we don't use remember_me
    assert len(client.cookie_jar) == 1

    ret = client.post('/api/logout/')
    assert ret.status_code == 200
    assert ret.json['message'] == 'user_logged_out'

    # non-existent user
    ret = client.post(
        '/api/login/',
        data={'email': 'foo@bar.baz', 'password': 'foo'}
    )
    assert ret.status_code == 401

    # existing user with wrong password
    ret = client.post(
        '/api/login/',
        data={'email': user.email, 'password': 'foo'}
    )
    assert ret.status_code == 401
    assert ret.json['message'] == 'invalid_credentials'

    ret = client.post('/api/logout/')
    assert ret.status_code == 200

    ret = client.post('/api/login/', data={**LOGIN_DATA, 'remember_me': True})
    assert ret.status_code == 200
    assert ret.json['message'] == 'user_logged_in'
    # with remember_me, we should have two cookies
    assert len(client.cookie_jar) == 2

    # logout user so the other tests have clean state
    client.post('/api/logout/')


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

    # logout user so the other tests have clean state
    client.post('/api/logout/')


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
    assert r.json['message'] == 'missing_role'
    assert r.json['role'] == 'test_role'

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

    # logout user so the other tests have clean state
    client.post('/api/logout/')


def test_current_user(client, user):
    assert client.get('/api/current_user/').status_code == 401
    assert client.post('/api/login/', data=LOGIN_DATA).status_code == 200
    r = client.get('/api/current_user/')
    assert r.json == {
        'name': 'Richard Feynman',
        'email_confirmed': True,
        'id': 1,
        'email': EMAIL,
        'roles': ['admin', 'test_role']
    }
