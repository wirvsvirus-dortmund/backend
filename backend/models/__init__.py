from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Shop(db.Model):
    ''' A shop '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.UnicodeText(), nullable=False)
    address = db.Column(db.UnicodeText(), nullable=False)
    capacity = db.Column(db.Integer)
    contact_info = db.Column(db.UnicodeText(), nullable=False)
