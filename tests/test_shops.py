def test_shops(app, client):
    from backend.models import db, Shop

    db.session.add(Shop(
        name='My Awesome Supermarket',
        capacity=50,
        contact_info='Richard Feynman\nrichard@feynman.org\n+49123456789',
        address='1234 Fermi Street\n56789 Los Alamos\nUSA',
    ))
    db.session.commit()

    assert Shop.query.count() == 1
    shop = Shop.query.first()
    assert shop.capacity == 50
    assert shop.name == 'My Awesome Supermarket'
