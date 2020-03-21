import pytest

@pytest.fixture(scope='module')
def shop(client):
    from backend.models import Shop, db

    shop = Shop(
        name='My Awesome Supermarket',
        capacity=50,
        contact_info='Richard Feynman\nrichard@feynman.org\n+49123456789',
        address='1234 Fermi Street\n56789 Los Alamos\nUSA',
    )
    db.session.add(shop)
    db.session.commit()
    return shop


def test_shop_api(client, shop):
    ret = client.get('/api/shops')
    test_store = ret.json[0]
    assert ret.status_code == 200
    assert test_store['name'] == 'My Awesome Supermarket'
    assert test_store['capacity'] == 50
    assert test_store['contact_info'] == 'Richard Feynman\nrichard@feynman.org\n+49123456789'
    assert test_store['address'] == '1234 Fermi Street\n56789 Los Alamos\nUSA'