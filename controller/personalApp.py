from flask import Blueprint
from flask_login import current_user, login_required

from .utils.response import HTTPResponse, HTTPError
from .utils.request import Request
from .utils.auth_required import AuthLevel, auth_required
from service.account import PasswordIncorrect

__all__ = ['personalApp_api']

personalApp_api = Blueprint('personalApp_api', __name__)


@personalApp_api.route('/changePassword', methods=['PUT'])
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


@personalApp_api.route('/changeNickname', methods=['PUT'])
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


@personalApp_api.route('/loadInfo', methods=['GET'])
def loadinfo():
    try:
        user = current_user.loadinfo()
        return HTTPResponse('loadinfo success', data=user)
    except:
        data = {
                "account_name": "",
                "nickname": "",
                "email": "",
                "auth": "3"}
        return HTTPResponse('loadinfo not login', data=data)