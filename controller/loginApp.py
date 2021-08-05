from flask import Blueprint, request
from service.account import Account
from http import HTTPStatus
from .auth import login_required
from .utils.response import HTTPResponse, HTTPError
from .utils.request import Request

__all__ = ['loginApp_api']

loginApp_api = Blueprint('loginApp_api', __name__)

@loginApp_api.route('/test', methods=['POST','GET'])
@login_required
def test():
    return HTTPResponse('test', 200)
    
@loginApp_api.route('/login', methods=['POST'])
@Request.json('username: str', 'password: str')
def login(username, password):
    #username = request.json['username']
    #password = request.json['password']
    print('ok')
   
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
@Request.json('username: str', 'password: str', 'email: str')
def signup(username, password, email):
   
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