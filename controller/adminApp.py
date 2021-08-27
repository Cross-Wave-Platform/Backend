from flask import Blueprint

from service.admin import *
from flask_login import login_user, logout_user, login_required
from .utils.response import HTTPResponse, HTTPError
from .utils.request import Request
from .utils.auth_required import auth_required,AuthLevel

__all__ = ['adminApp_api']

adminApp_api = Blueprint('adminApp_api', __name__)

@adminApp_api.route('/user_management', methods=['GET'])
@login_required
@auth_required(AuthLevel.ADMIN)
@Request.json('Identity: str')
def user_management(Identity):
    try:
        user = user_management(Identity)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('ok', list = user)

@adminApp_api.route('/change_auth', methods=['PUT'])
@login_required
@auth_required(AuthLevel.ADMIN)
@Request.json('user: str', 'userlevel: str')
def change_auth(user, userlevel):
    try:
        change_auth(user, userlevel)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('ok')

@adminApp_api.route('/auth', methods=['GET'])
@login_required
@auth_required(AuthLevel.ADMIN)
@Request.json('auth: str')
def search_by_auth(auth):
    try:
        list = search_by_auth(auth)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('ok', list=list)

@adminApp_api.route('/month', methods=['GET'])
@login_required
@auth_required(AuthLevel.ADMIN)
@Request.json('month: str')
def search_by_month(month):
    try:
        list = search_by_month(month)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('ok', list=list)

@adminApp_api.route('/wave', methods=['GET'])
@login_required
@auth_required(AuthLevel.ADMIN)
@Request.json('wave: str')
def search_by_wave(wave):
    try:
        list = search_by_wave(wave)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('ok', list=list)

@adminApp_api.route('/type', methods=['GET'])
@login_required
@auth_required(AuthLevel.ADMIN)
@Request.json('type: str')
def search_by_type(type):
    try:
        list = search_by_type(type)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('ok', list=list)

@adminApp_api.route('/keyword', methods=['GET'])
@login_required
@auth_required(AuthLevel.ADMIN)
@Request.json('keyword: str')
def search_by_keyword(keyword):
    try:
        list = search_by_keyword(keyword)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('ok', list=list)