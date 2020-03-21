from backend import create_app
from backend.models import db, User, Shop, CustomerDatapoint
from datetime import datetime, timedelta
import random


with create_app().app_context():
    u = User(username='rfeynman', email='richard@feynman.org')
    u.set_password('los-alamos')
    db.session.add(u)

    shop = Shop(
        name='My Awesome Supermarket',
        capacity=50,
        contact_info='Richard Feynman\nrichard@feynman.org\n+49123456789',
        address='1234 Fermi Street\n56789 Los Alamos\nUSA',
    )
    db.session.add(shop)
    db.session.commit()

    for i in range(10):
        db.session.add(CustomerDatapoint(
            shop_id=shop.id,
            timestamp=datetime.now() + timedelta(minutes=15 * i),
            customers_inside=random.randint(20, 60),
            queue_size=random.randint(0, 20),
        ))

    db.session.commit()
