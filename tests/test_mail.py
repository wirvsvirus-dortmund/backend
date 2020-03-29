def test_mails(app):
    from backend.mail import mail, send_email

    with mail.record_messages() as outbox:
        send_email(
            recipients='test@example.org',
            subject='Test Email',
            body='Welcome to supermarkt.org',
        )

    assert len(outbox) == 1
    email = outbox[0]
    assert email.subject == 'Test Email'
    assert email.body == 'Welcome to supermarkt.org'
    assert len(email.recipients) == 1
    assert 'test@example.org' in email.recipients
    assert email.sender == 'Supermarkt <supermarkt@test.org>'
