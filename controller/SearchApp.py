from flask import Blueprint
from flask_login import login_required, current_user
from service.search import Search
from .utils.response import HTTPResponse, HTTPError
from .utils.request import Request

__all__ = ['searchApp_api']

searchApp_api = Blueprint('searchApp_api',__name__)

#get waves from selected age and survey type
@searchApp_api.route('/SearchWave', methods=['GET'])
@Request.args('ageType','surveyType')
def searchWave(ageType, surveyType):
    try:
        wave = Search.search_wave(ageType, surveyType)
        if wave == 'not found':
            return HTTPError('Wave not found', 404)
    except:
        return HTTPError('unknown error', 406)

    return HTTPResponse('ok', data={"wave":wave})

#get problems from selected age, survey, wave 
@searchApp_api.route('/SearchInfo', methods=['GET'])
@login_required
# @Request.args('age_type', 'survey_type', 'wave')
def searchInfo():
    try:
        Info = Search.search_info(current_user.id)
        if not Info:
            return HTTPError('Info not found', 404)
    except:
        return HTTPError('unknown error', 406)

    return HTTPResponse('ok', data=Info)

#get user's last search info: age, survey type
@searchApp_api.route('/GetSearchInfo', methods=['GET'])
@login_required
def getSearchInfo():
    try:
        Info = Search.get_search_info(current_user.id)
        if Info == 'not found':
            return HTTPError('Info not found', 404)
    except:
        return HTTPError('unknown error', 406)
    
    return HTTPResponse('ok', data={"info":Info})

#store user's last search info: age, survey type
@searchApp_api.route('/StoreSearchInfo', methods=['POST'])
@login_required
@Request.json('info: dict')
def storeSearchInfo(info):
    try:
        res = Search.store_search_info(current_user.id, info)
        if res == 'Fail':
            return HTTPError('Failed to store search info', 405)
    except:
        return HTTPError('unknown error', 406)
    
    return HTTPResponse('ok')

#delete user's search info: age, survey type
@searchApp_api.route('/DelSearchInfo', methods=['DELETE'])
@login_required
def delSearchInfo():
    try:
        Info = Search.del_search_info(current_user.id)
    except:
        return HTTPError('unknown error', 406)
    
    return HTTPResponse('ok')

#store user's selected probelm to shop_cart
@searchApp_api.route('/StoreInfo', methods=['POST'])
@login_required
@Request.json('problemList: list')
def storeInfo(problemList):
    try:
        res = Search.store_info(current_user.id, problemList)
        if res == 'failed':
            return HTTPError('Failed to store info', 403)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('ok')

#get user's shop_cart
@searchApp_api.route('/GetInfo', methods=['GET'])
@login_required
def getInfo():
    try:
        problem_list = Search.get_info(current_user.id)
        if not problem_list:
            return HTTPError('Failed to fetch info', 403)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('ok', data={"problemList":problem_list})

#delete user's shop_cart
@searchApp_api.route('/DelInfo', methods=['DELETE'])
@login_required
def delInfo():
    try:
        '''delete user info'''
        res = Search.del_info(current_user.id)
        if  not res:
            return HTTPError('Failed to delete info', 403)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('ok')