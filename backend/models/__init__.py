from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


__all__ = ['db', 'Shop', 'User']


db = SQLAlchemy()


class Shop(db.Model):
    ''' A shop '''
    __tablename__ = 'shops'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.UnicodeText(), nullable=False)
    address = db.Column(db.UnicodeText(), nullable=False)
    capacity = db.Column(db.Integer)
    contact_info = db.Column(db.UnicodeText(), nullable=False)

    def __repr__(self):
        return f'<Shop {self.id}: {self.name}>'


class User(db.Model, UserMixin):
    '''
    User class / model for authentication

    Two cases are foreseen at the moment:
    Admin users and shop employees for reporting.
    '''
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.UnicodeText(), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    email_confirmed = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.id}: {self.username}>'
