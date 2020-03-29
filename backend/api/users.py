from flask import render_template, current_app
from flask_restful import Resource, reqparse
from itsdangerous import URLSafeSerializer
from sqlalchemy.exc import IntegrityError

from ..models import db, User
from ..mail import send_email
from ..utils import ext_url_for, json_abort


class UsersAPI(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('name', required=True)
    parser.add_argument('email', required=True)
    parser.add_argument('password', required=True)

    def post(self):
        '''Adds a new user'''
        args = self.parser.parse_args()

        password = args.pop('password')
        new_user = User(**args)
        new_user.set_password(password)
        db.session.add(new_user)

        try:
            db.session.commit()
        except IntegrityError as e:
            if 'UNIQUE constraint failed: users.email' in str(e):
                json_abort(422, message='email_taken')
            else:
                raise
        finally:
            db.session.rollback()

        # send email verification link
        ts = URLSafeSerializer(current_app.config["SECRET_KEY"], salt='verify-email')
        token = ts.dumps(new_user.id)
        link = ext_url_for('auth.verify_email', token=token)

        send_email(
            new_user.email,
            'Registrierung bei Supermarkt abschließen',
            render_template('registration.txt', validation_link=link, name=new_user.name)
        )

        return dict(message='verify_email', user=new_user.as_dict()), 201
