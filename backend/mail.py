from flask import current_app
from flask_mail import Mail, Message
from threading import Thread
import socket
import logging
import backoff


log = logging.getLogger(__name__)

socket.setdefaulttimeout(30)
mail = Mail()


def send_msg_async(msg):
    '''
    Calls a mail.send(msg) in a background thread.
    Retries on errors using exponential backoff.
    See https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-x-email-support
    '''
    def on_backoff(details):
        msg = 'Sending email failed in {tries} attempt, waiting {wait:.1f} s.'
        log.error(msg.format(**details))

    @backoff.on_exception(
        backoff.expo,
        Exception,
        max_tries=18,
        on_backoff=on_backoff,
    )
    def target(app, mail):
        log.info(f'Sending mail with subject "{msg.subject}" to {msg.recipients}')
        with app.app_context():
            try:
                mail.send(msg)
            except Exception:
                logging.exception('Failed sending mail')
                raise
        log.info('Mail sent')

    # noqa: See https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure
    # For an explanation of the current_app magic
    Thread(
        target=target,
        args=(current_app._get_current_object(), msg)
    ).start()


def send_email(recipients, subject, body, **kwargs):
    '''
    Send an email async using a background thread
    '''
    # enclose single recipient in a list as required by flask_mail
    if isinstance(recipients, str):
        recipients = [recipients]

    msg = Message(
        subject=subject,
        sender=current_app.config['MAIL_SENDER'],
        recipients=recipients,
        **kwargs
    )
    msg.body = body

    # capturing mails does not work in another thread
    # so just send it here for the unit tests
    if current_app.config['TESTING']:
        mail.send(msg)
    # When debugging, just send it
    elif current_app.config['DEBUG'] is True:
        print('Sender:     ', current_app.config['MAIL_SENDER'])
        print('Recipients: ', recipients)
        print('Subject:    ', subject)
        print(body)
    # if in production, use background thread
    else:
        send_msg_async(msg)
