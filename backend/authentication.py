from functools import wraps

from flask_login import (
    LoginManager,
    login_user, logout_user,
    login_required, current_user,
)
from flask import jsonify, Blueprint, abort, make_response

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired


from .models import User


auth = Blueprint('auth', __name__)
login = LoginManager()


def json_abort(status_code, **kwargs):
    '''Abort current session with `status_code` and send a json response as
    object containing `**kwargs`'''
    return abort(make_response(jsonify(**kwargs), status_code))


def role_required(role_name):
    '''
    Check if current_user has a role named `role_name`.
    Abort request with 401, if that's not the case.

    Usage:
        Decorate view function (`app.route(...)`) with this decorator and
        specify a name of a role.
        The name will be compared to all roles of the current_user.
    '''
    def access_decorator(func):
        @wraps(func)
        @login_required  # first of all a use needs to be logged in
        def decorated_function(*args, **kwargs):
            if not current_user.has_role(role_name):
                return json_abort(401, message='missing_role', role=role_name)
            return func(*args, **kwargs)
        return decorated_function
    return access_decorator


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@login.unauthorized_handler
def handle_needs_login():
    return json_abort(401, message='login_required')


class LoginForm(FlaskForm):
    username = StringField('Nutzername/Email', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    remember_me = BooleanField('Eingeloggt bleiben?')
    submit = SubmitField('Login')


@auth.route('/login/', methods=['POST'])
def login_endpoint():
    '''
    Login a user
    '''
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()

        if user is None or not user.check_password(form.password.data):
            return json_abort(401, message='invalid_credentials')

        if not user.email_confirmed:
            json_abort(401, message='unconfirmed_email')

        login_user(user, remember=form.remember_me.data)

        return jsonify(message='user_logged_in')
    return json_abort(401, message='invalid_input', errors=form.errors)


@auth.route('/logout/', methods=['POST'])
def logout():
    logout_user()
    return jsonify(message='user_logged_out')


@auth.route('/current_user/')
@login_required
def get_current_user():
    return current_user.as_dict()
