from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .database import db


class Role(db.Model):
    '''
    Roles are for access management.
    Certain endpoints require the user to have a certain role to be able to access it.
    '''
    __tablename__ = 'roles'

    name = db.Column(db.String(30), primary_key=True)

    def __repr__(self):
        return f'<Role: {self.name}>'


# the many-to-many table that assigns roles to users
user_roles = db.Table(
    'user_roles',
    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    ),
    db.Column(
        'role_name',
        db.String(30),
        db.ForeignKey('roles.name'),
        primary_key=True
    )
)


class User(db.Model, UserMixin):
    '''
    User class / model for authentication

    Two cases are foreseen at the moment:
    Admin users and shop employees for reporting.
    '''
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.UnicodeText(), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    email_confirmed = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128))

    roles = db.relationship(
        'Role',
        secondary=user_roles,
        lazy='joined',
        backref=db.backref('users', lazy=True)
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, role_name):
        for role in self.roles:
            if role_name == role.name:
                return True
        return False

    def as_dict(self):
        d = super().as_dict()
        del d['password_hash']
        d['roles'] = [r.name for r in self.roles]
        return d

    def __repr__(self):
        return f'<User {self.id}: {self.username}>'
