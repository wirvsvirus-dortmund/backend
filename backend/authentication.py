from functools import wraps

from flask_login import (
    LoginManager,
    login_user, logout_user,
    login_required, current_user,
)
from flask import (
    jsonify, Blueprint, abort, current_app, redirect, render_template,
)
from itsdangerous import URLSafeSerializer, BadData

from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


from .models import User, db
from .mail import send_email
from .utils import json_abort


auth = Blueprint('auth', __name__)
login = LoginManager()


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
    email = EmailField('Nutzername/Email', validators=[DataRequired()])
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
        email = form.email.data
        user = User.query.filter(User.email == email).first()

        if user is None or not user.check_password(form.password.data):
            return json_abort(401, message='invalid_credentials')

        if not user.email_confirmed:
            json_abort(401, message='unconfirmed_email')

        login_user(user, remember=form.remember_me.data)

        return jsonify(message='user_logged_in')
    return json_abort(401, message='invalid_input', errors=form.errors)


@auth.route('/logout/', methods=['POST', 'GET'])
def logout():
    logout_user()
    return jsonify(message='user_logged_out')


@auth.route('/csrf_token/')
def get_csrf_token():
    form = LoginForm()
    return jsonify(token=form.csrf_token.current_token)


@auth.route('/current_user/')
@login_required
def get_current_user():
    return current_user.as_dict()


@auth.route('/verify_email/<token>')
def verify_email(token):
    ts = URLSafeSerializer(
        current_app.config["SECRET_KEY"],
        salt='verify-email',
    )
    try:
        user_id = ts.loads(token)
    except BadData:
        abort(404)

    user = User.query.get_or_404(user_id)
    user.email_confirmed = True
    db.session.add(user)
    db.session.commit()

    send_email(
        user.email,
        'Supermarkt-Status Registrierung abgeschlossen',
        render_template('confirmed.txt', name=user.name),
    )

    return redirect('/')
