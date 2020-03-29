from flask import url_for, current_app


def ext_url_for(*args, **kwargs):
    '''Send an external link with the correct protocol (https or http)'''
    return url_for(
        *args, **kwargs,
        _external=True,
        _scheme='https' if current_app.config['USE_HTTPS'] else 'http',
    )
