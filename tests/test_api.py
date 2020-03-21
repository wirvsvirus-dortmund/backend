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


def test_ShopAPI(client, shop):
    ret = client.get('/shops')
    assert ret.status_code == 200
    assert ret.json[0]['name'] == 'My Awesome Supermarket'