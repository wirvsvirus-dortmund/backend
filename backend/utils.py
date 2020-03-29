from flask import url_for, current_app, jsonify, abort, make_response


def ext_url_for(*args, **kwargs):
    '''Send an external link with the correct protocol (https or http)'''
    return url_for(
        *args, **kwargs,
        _external=True,
        _scheme='https' if current_app.config['USE_HTTPS'] else 'http',
    )


def json_abort(status_code, **kwargs):
    '''Abort current session with `status_code` and send a json response as
    object containing `**kwargs`'''
    return abort(make_response(jsonify(**kwargs), status_code))
