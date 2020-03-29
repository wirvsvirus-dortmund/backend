from backend import create_app
from backend.models import db, User, Shop, CustomerDatapoint
from datetime import datetime, timedelta
import random
from getpass import getpass


with create_app().app_context():
    print('Creating user')
    name = input('Name: ')
    email = input('Email: ')

    password = None
    confirmed = False

    while not confirmed:
        password = getpass('Password: ')
        confirm = getpass('Confirm Password: ')
        confirmed = confirm == password
        if not confirmed:
            print('Passwords do not match')

    u = User(name=name, email=email)
    u.set_password(password)
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
