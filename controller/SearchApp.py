from flask import Blueprint, request
from flask_login import login_required, current_user
from flask_login.utils import login_fresh
from service.search import Search
from .utils.response import HTTPResponse, HTTPError
from .utils.request import Request

__all__ = ['SearchApp_api']

SearchApp_api = Blueprint('SearchApp_api',__name__)

def conv_req_list(params_str):
    str_list=request.args.getlist(params_str)
    return list(map(int,str_list))

#get waves from selected age and survey type
@SearchApp_api.route('/SearchWave', methods=['GET'])
def searchWave():
    try:
        ageType = conv_req_list("ageType")
        surveyType = conv_req_list('surveyType')
        wave = Search.search_wave(ageType, surveyType)
        # if wave == 'not found':
        #     return HTTPError('Wave not found', 404)
    except:
        return HTTPError('unknown error', 406)

    return HTTPResponse('ok', data={"wave":wave})

#get problems from selected age, survey, wave 
@SearchApp_api.route('/SearchInfo', methods=['GET'])
@login_required
def searchInfo():
    try:
        Info = Search.search_info(current_user.id)
        # if not Info:
        #     return HTTPError('Info not found', 404)
    except:
        return HTTPError('unknown error', 406)
    
    return HTTPResponse('ok', data={"info":Info})

#get user's last search info: age, survey type
@SearchApp_api.route('/GetSearchInfo', methods=['GET'])
@login_required
def getSearchInfo():
    try:
        Info = Search.search_info(current_user.id)
        # if Info == 'not found':
        #     return HTTPError('Info not found', 404)
    except:
        return HTTPError('unknown error', 406)
    
    return HTTPResponse('ok', data={"info":Info})

#store user's last search info: age, survey type
@SearchApp_api.route('/StoreSearchInfo', methods=['POST'])
@login_required
@Request.json('info: dict')
def storeSearchInfo(info):
    try:
        res = Search.store_search_info(current_user.id, info)
        # if res == 'Fail':
        #     return HTTPError('Failed to store search info', 405)
    except:
        return HTTPError('unknown error', 406)
    
    return HTTPResponse('ok')

#delete user's search info: age, survey type
@SearchApp_api.route('/DelSearchInfo', methods=['DELETE'])
@login_required
def delSearchInfo():
    try:
        Search.del_search_info(current_user.id)
    except:
        return HTTPError('unknown error', 406)
    
    return HTTPResponse('ok')

#store user's selected probelm to shop_cart
@SearchApp_api.route('/StoreInfo', methods=['POST'])
@login_required
@Request.json('problemList: list')
def storeInfo(problemList):
    try:
        Search.store_info(current_user.id, problemList)
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
        problem_id = Search.get_info(current_user.id)
        # if problem_id == 'failed':
        #     return HTTPError('Failed to fetch info', 403)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('ok', problem_id=problem_id)

#delete user's shop_cart
@SearchApp_api.route('/DelInfo', methods=['DELETE'])
@login_required
def delInfo():
    try:
        '''delete user info'''
        Search.del_info(current_user.id)
        # if  res == 'failed':
        #     return HTTPError('Failed to delete info', 403)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('ok')