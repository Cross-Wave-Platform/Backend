import flask
from flask import Blueprint, request
from database.account import Account

__all__ = ['loginApp_api']

loginApp_api = Blueprint('loginApp_api', __name__)

@loginApp_api.route('/login', methods=['POST'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    try:
        user = Account.login(username, password)
    except:
        #return HTTPError
        return 0