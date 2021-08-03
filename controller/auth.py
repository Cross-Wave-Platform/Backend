from functools import wraps
from flask import Blueprint, request
from service.account import Account, jwt_decode
from .utils.response import HTTPError, HTTPResponse
from .utils.request import Request

__all__ = ['auth_api', 'login_required']

auth_api = Blueprint('auth_api', __name__)

def login_required(func):
    '''Check if the user is login

    Returns:
        - A wrapped function
        - 403 Not Logged In
        - 403 Invalid Token
        - 403 Inactive User
    '''
    @wraps(func)
    @Request.cookies(vars_dict={'token': 'piann'})
    def wrapper(token, *args, **kwargs):
        if token is None:
            return HTTPError('Not Logged In', 403)
        json = jwt_decode(token)
        if json is None or not json.get('secret'):
            return HTTPError('Invalid Token', 403)
        user = Account(json['data']['username'])
        if json['data'].get('userId') != user.user_id:
            return HTTPError(f'Authorization Expired', 403)
        if not user.active:
            return HTTPError('Inactive User', 403)
        kwargs['user'] = user
        return func(*args, **kwargs)

    return wrapper