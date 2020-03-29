import re


def test_registration(client):
    from backend.mail import mail

    with mail.record_messages() as outbox:
        ret = client.post('/api/users', data={
            'name': 'Enrico Fermi',
            'email': 'enrico@fermi.org',
            'password': 'half-spin',
        })
        assert ret.status_code == 201

    # test mail was send
    assert len(outbox) == 1
    assert 'Enrico Fermi' in outbox[0].body

    # email not verified yet
    r = client.post('/api/login/', data={
        'email': 'enrico@fermi.org', 'password': 'half-spin'
    })
    assert r.status_code == 401
    assert r.json['message'] == 'unconfirmed_email'

    # get verification link from body
    m = re.search(r'http(s)?:\/\/.*(\/api\/verify_email\/.*)', outbox[0].body)
    assert m
    link = m.group(2)

    with mail.record_messages() as outbox:
        assert client.get(link)

    assert len(outbox) == 1
    email = outbox[0]
    assert email.subject == 'Supermarkt-Status Registrierung abgeschlossen'

    # now it should work
    r = client.post('/api/login/', data={
        'email': 'enrico@fermi.org', 'password': 'half-spin'
    })
    assert r.status_code == 200
