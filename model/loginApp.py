import flask
from flask import Blueprint, request
from database.account import Account
from http import HTTPStatus

__all__ = ['loginApp_api']

loginApp_api = Blueprint('loginApp_api', __name__)

@loginApp_api.route('/test', methods=['POST'])
def test():
    return {"test": True}, HTTPStatus.OK
    
@loginApp_api.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
   
    try:
        user = Account.login(username, password)
        if user == 'user not found':
            return {}, HTTPStatus.NOT_FOUND
        elif user == 'password incorrect':
            return {}, HTTPStatus.NOT_ACCEPTABLE
    except:
        return {}, HTTPStatus.FORBIDDEN

    return {'user':user.username}, HTTPStatus.OK

@loginApp_api.route('/register', methods=['POST'])
def signup():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    print("signup: ", username, password, email)

    try:
        user = Account.signup(username, password, email)
    except:
        #return HTTPError
        return 0