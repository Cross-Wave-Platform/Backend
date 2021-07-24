import flask
from flask import Blueprint, request
from database.account import Account

__all__ = ['loginApp_api']

loginApp_api = Blueprint('loginApp_api', __name__)

@loginApp_api.route('/test', methods=['POST'])
def test():
    return {"ok":"ok"}, 200
    
@loginApp_api.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    print("login: ", username, password)

    try:
        user = Account.login(username, password)
    except:
        #return HTTPError
        return 0

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