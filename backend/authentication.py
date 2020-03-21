from flask_login import LoginManager, login_user, logout_user
from flask import jsonify, abort, redirect, url_for, flash, Blueprint

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


from .models import User


auth = Blueprint('auth', __name__)
login = LoginManager()


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@login.unauthorized_handler
def handle_needs_login():
    return jsonify(
        status='access_denied',
        message='You need to login to access this page'
    ), 401


class LoginForm(FlaskForm):
    username = StringField('Nutzername/Email', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired()])
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
            flash('Invalid user or password', 'danger')
            return jsonify(status='error', message='invalid user or password'), 401

        login_user(user)

        return jsonify(status='success', message='user logged in')
    return jsonify(status='error', message='invalid form input', errors=form.errors), 401


@auth.route('/logout/', methods=['POST'])
def logout():
    logout_user()
    return jsonify(status='success', message='user logged out')
