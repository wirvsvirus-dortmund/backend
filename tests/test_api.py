import pytest
from datetime import datetime


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
    test_store = ret.json['shops'][0]
    assert ret.status_code == 200
    assert ret.json['status'] == 'success'
    assert test_store['name'] == 'My Awesome Supermarket'
    assert test_store['capacity'] == 50
    assert test_store['contact_info'] == 'Richard Feynman\nrichard@feynman.org\n+49123456789'
    assert test_store['address'] == '1234 Fermi Street\n56789 Los Alamos\nUSA'


def test_shopdata_api(client, shop):
    # non existing shop
    ret = client.get('/api/shops/150/data')
    assert ret.status_code == 404
    assert ret.json['message'] == 'Shop with id 150 does not exist'

    ret = client.get(f'/api/shops/{shop.id}/data')
    assert ret.status_code == 200
    assert ret.json['status'] == 'success'
    # no data yet
    assert len(ret.json['customers']) == 0

    ts = datetime.now().isoformat()
    # add data
    ret = client.post(f'/api/shops/{shop.id}/data', data={
        'timestamp': ts,
        'customers_inside': 50,
        'queue_size': 10,
    })
    assert ret.status_code == 201

    ret = client.get(f'/api/shops/{shop.id}/data')
    assert ret.status_code == 200
    assert ret.json['status'] == 'success'

    assert len(ret.json['customers']) == 1
    data = ret.json['customers'][0]
    assert data['id'] == 1
    assert data['timestamp'] == ts
    assert data['customers_inside'] == 50
    assert data['queue_size'] == 10
