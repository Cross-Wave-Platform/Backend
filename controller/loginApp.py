from flask import Blueprint, request
from model.account import Account
from .auth import login_required
from .utils.response import HTTPResponse, HTTPError

__all__ = ['loginApp_api']

loginApp_api = Blueprint('loginApp_api', __name__)

@loginApp_api.route('/test', methods=['POST'])
@login_required
def test():
    return HTTPResponse('test', 200)
    
@loginApp_api.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
   
    try:
        user = Account.login(username, password)
        if user == 'user not found':
            return HTTPError('user not found', 404)
        elif user == 'password incorrect':
            return HTTPError('password incorrect', 403)
    except:
        return HTTPError('unknown error', 406)
    
    cookies = {'piann_httponly': user.secret, 'jwt': user.cookie}

    return HTTPResponse('Login success', cookies=cookies)

@loginApp_api.route('/register', methods=['POST'])
def signup():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    print("signup: ", username, password, email)

    try:
        user = Account.signup(username, password, email)
        if user == 'email used':
            return HTTPError('email used', 403)
        elif user == 'account exists':
            return HTTPError('account exists', 404)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('sugnup success')