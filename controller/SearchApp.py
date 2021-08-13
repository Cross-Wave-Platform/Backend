from flask import Blueprint
from flask_login import login_required, current_user
from service.account import Account
from service.search import search_wave, search_info, store_info, get_info
from .utils.response import HTTPResponse, HTTPError
from .utils.request import Request

__all__ = ['SearchApp_api']

SearchApp_api = Blueprint('SearchApp_api',__name__)


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

@SearchApp_api.route('/StoreInfo', methods=['POST'])
@login_required
@Request.json('problem_id: str[]')
def storeInfo(problem_id):
    try:
        res = store_info(current_user.username, problem_id)
        # if res == 'failed':
        #     return HTTPError('Failed to store info', 403)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('ok')

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

@SearchApp_api.route('/DelInfo', methods=['GET'])
@login_required
def delInfo():
    try:
        '''delete user info'''
        user = current_user.username
        res = 'sql delete shop_cart'
        if  res == 'failed':
            return HTTPError('Failed to fetch info', 403)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('ok')