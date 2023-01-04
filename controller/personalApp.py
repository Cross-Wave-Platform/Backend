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


@personalApp_api.route('/changeName', methods=['PUT'])
@login_required
@auth_required(AuthLevel.REGULAR)
@Request.json('newName: str')
def change_name(newName):
    try:
        change = current_user.change_name(newName)
    except:
        return HTTPError('unknown error', 406)
    current_user.name = change.name
    return HTTPResponse('change name success')


@personalApp_api.route('/changePhone', methods=['PUT'])
@login_required
@auth_required(AuthLevel.REGULAR)
@Request.json('newPhone: str')
def change_phone(newPhone):
    try:
        change = current_user.change_phone(newPhone)
    except:
        return HTTPError('unknown error', 406)
    current_user.phone = change.phone
    return HTTPResponse('change phone success')


@personalApp_api.route('/changeOrganization', methods=['PUT'])
@login_required
@auth_required(AuthLevel.REGULAR)
@Request.json('newOrganization: str')
def change_organization(newOrganization):
    try:
        change = current_user.change_organization(newOrganization)
    except:
        return HTTPError('unknown error', 406)
    current_user.organization = change.organization
    return HTTPResponse('change organization success')


@personalApp_api.route('/changeRelation', methods=['PUT'])
@login_required
@auth_required(AuthLevel.REGULAR)
@Request.json('newRelation: int')
def change_relation(newRelation):
    try:
        change = current_user.change_relation(newRelation)
    except:
        return HTTPError('unknown error', 406)
    current_user.relation = change.relation
    return HTTPResponse('change relation success')


@personalApp_api.route('/loadInfo', methods=['GET'])
def loadinfo():
    try:
        user = current_user.loadinfo()
        return HTTPResponse('loadinfo success', data=user)
    except:
        data = {
                "account_name": None,
                "nickname": None,
                "email": None,
                "auth": 3}
        return HTTPResponse('loadinfo not login', data=data)