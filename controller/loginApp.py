from flask import Blueprint
from service.account import Account, AccountUsed, EmailUsed, UserNotFound, PasswordIncorrect, UserRegister
from flask_login import login_user, logout_user, login_required
from service.report import Send_Email
from .utils.response import HTTPResponse, HTTPError
from .utils.request import Request

__all__ = ['loginApp_api']

loginApp_api = Blueprint('loginApp_api', __name__)

@loginApp_api.route('/login', methods=['POST'])
@Request.json('username: str', 'password: str')
def login(username, password):
    try:
        user = Account.login(username, password)
    except UserNotFound:
        return HTTPError('user not found', 404)
    except PasswordIncorrect:
        return HTTPError('password incorrect', 403)
    except:
        return HTTPError('unknown error', 406)
    login_user(user)
    return HTTPResponse('login success')


@loginApp_api.route('/register', methods=['POST'])
@Request.json('username: str', 'password: str', 'email: str')
def signup(username, password, email):
    try:
        s = Account.signup(username, password, email)
    except EmailUsed:
        return HTTPError('email used', 403)
    except AccountUsed:
        return HTTPError('account exists', 404)
    except ValueError:
        return HTTPError('illegal characters in username', 405)
    except:
        return HTTPError('unknown error', 406)

    mymail = Send_Email('Welcome to KIT waves, please verify your email.', [email])
    try:
        mymail.htmladd('<a href="http://localhost:8080/verify/' + s + '">驗證網址</a>')
        #print('http://localhost:8080/verify/' + s)
        mymail.send()
    except Exception as e:
        return HTTPError(str(e), 406)

    return HTTPResponse('signup success')

@loginApp_api.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return HTTPResponse('logout success')

@loginApp_api.route('/user_confirm', methods=['POST'])
@Request.json('token: str')
def user_confirm(token):
    user = UserRegister()
    validated = user.validate_confirm_token(token)
    if validated:
        return HTTPResponse('Thands For Your Activate')
    else:
        return HTTPError('wrong token', 403)