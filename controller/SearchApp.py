from flask import Blueprint
from flask_login import login_required, current_user
from service.account import Account
from service.search import *
from .utils.response import HTTPResponse, HTTPError
from .utils.request import Request

__all__ = ['SearchApp_api']

SearchApp_api = Blueprint('SearchApp_api',__name__)

#get waves from selected age and survey type
@SearchApp_api.route('/SearchWave', methods=['GET'])
@Request.json('age_type: int','survey_type: int')
def searchWave(age_type, survey_type):
    try:
        wave = search_wave(age_type, survey_type)
        if wave == 'not found':
            return HTTPError('Wave not found', 404)
    except:
        return HTTPError('unknown error', 406)

    return HTTPResponse('ok', wave=wave)

#get problems from selected age, survey, wave 
@SearchApp_api.route('/SearchInfo', methods=['GET'])
@Request.json('age_type: int', 'survey_type: int', 'wave: int')
def searchWave(age_type, survey_type, wave):
    try:
        Info = search_info(age_type,survey_type, wave)
        if Info == 'not found':
            return HTTPError('Info not found', 404)
    except:
        return HTTPError('unknown error', 406)
    
    return HTTPResponse('ok', info=Info)

#get user's last search info: age, survey type
@SearchApp_api.route('/GetSearchInfo', methods=['GET'])
@login_required
def getSearchInfo():
    try:
        Info = search_info(current_user.username)
        if Info == 'not found':
            return HTTPError('Info not found', 404)
    except:
        return HTTPError('unknown error', 406)
    
    return HTTPResponse('ok', info=Info)

#store user's selected probelm to shop_cart
@SearchApp_api.route('/StoreInfo', methods=['POST'])
@login_required
@Request.json('problem_id: list')
def storeInfo(problem_id):
    try:
        res = store_info(current_user.username, problem_id)
        # if res == 'failed':
        #     return HTTPError('Failed to store info', 403)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('ok')

#get user's shop_cart
@SearchApp_api.route('/GetInfo', methods=['GET'])
@login_required
def getInfo():
    try:
        problem_id = get_info(current_user.username)
        if problem_id == 'failed':
            return HTTPError('Failed to fetch info', 403)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('ok', problem_id=problem_id)

#delete user's shop_cart
@SearchApp_api.route('/DelInfo', methods=['GET'])
@login_required
@Request.json('problem_id: list')
def delInfo(problem_id):
    try:
        '''delete user info'''
        user = current_user.username
        res = del_info(user, problem_id)
        if  res == 'failed':
            return HTTPError('Failed to fetch info', 403)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('ok')