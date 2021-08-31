from flask import Blueprint
from service.account import Account
from flask_login import login_user, logout_user, login_required
from .utils.response import HTTPResponse, HTTPError
from .utils.request import Request

__all__ = ['loginApp_api']

loginApp_api = Blueprint('loginApp_api', __name__)

@loginApp_api.route('/login', methods=['POST'])
@Request.json('username: str', 'password: str')
def login(username, password):
    try:
        user = Account.login(username, password)
        if user == 'user not found':
            return HTTPError('user not found', 404)
        elif user == 'password incorrect':
            return HTTPError('password incorrect', 403)
    except:
        return HTTPError('unknown error', 406)
    login_user(user)
    return HTTPResponse('Login success')


@loginApp_api.route('/register', methods=['POST'])
@Request.json('username: str', 'password: str', 'email: str')
def signup(username, password, email):

    try:
        user = Account.signup(username, password, email)
        if user == 'email used':
            return HTTPError('email used', 403)
        elif user == 'account exists':
            return HTTPError('account exists', 404)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('sugnup success')


@loginApp_api.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return HTTPResponse('logout success')
