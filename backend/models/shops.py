from .database import db


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


class CustomerDatapoint(db.Model):
    '''
    A time series data point for information about a shop at a given time
    '''
    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey(Shop.id))
    timestamp = db.Column(db.TIMESTAMP(timezone=True))
    customers_inside = db.Column(db.Integer)
    queue_size = db.Column(db.Integer)

    def __repr__(self):
        return (
            f'<{self.__class__.__name__}:'
            f' {self.timestamp.isoformat()}'
            f', inside={self.customers_inside}'
            f', queue={self.queue_size}'
            '>'
        )
