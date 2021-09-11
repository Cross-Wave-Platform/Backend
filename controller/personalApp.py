from flask import Blueprint
from flask_login import current_user, login_required

from .utils.response import HTTPResponse, HTTPError
from .utils.request import Request
from .utils.auth_required import AuthLevel, auth_required
from service.account import PasswordIncorrect

__all__ = ['personalApp_api']

personalApp_api = Blueprint('personalApp_api', __name__)


@personalApp_api.route('/changepassword', methods=['PUT'])
@login_required
@auth_required(AuthLevel.REGULAR)
@Request.json('oldPassword: str', 'newPassword: str')
def change_password(oldPassword, newPassword):
    try:
        change = current_user.change_password(oldPassword, newPassword)
    except PasswordIncorrect:
        return HTTPError('password incorrect', 403)
    except:
        return HTTPError('unknown error', 406)
    current_user.password = change.password
    return HTTPResponse('change password success')

@personalApp_api.route('/changenickname', methods=['PUT'])
@login_required
@auth_required(AuthLevel.REGULAR)
@Request.json('newNickname: str')
def change_nickname(newNickname):
    try:
        change = current_user.change_nickname(newNickname)
    except:
        return HTTPError('unknown error', 406)
    current_user.nickname = change.nickname
    return HTTPResponse('change nickname success')

@personalApp_api.route('/loadinfo', methods=['GET'])
@login_required
@auth_required(AuthLevel.REGULAR)
def loadinfo():
    try:
        user = current_user.loadinfo()
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('loadinfo success', data=user)