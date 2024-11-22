from functools import wraps

from flask import session
from flask import jsonify


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('logged_in') is None:
            return jsonify({'message': 'Para usar este recurso es necesario estar loggeado.'}), 401
        return func(*args, **kwargs)
    return wrapper
