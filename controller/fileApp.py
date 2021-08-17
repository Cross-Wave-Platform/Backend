import os
from flask import send_file, Blueprint, request
from flask_login import current_user
from http import HTTPStatus
from flask_login import login_required
from service.account import Account
from service.upload import Upload_Files
from service.export import Export_Files
from .utils.response import HTTPResponse, HTTPError
from .utils.request import Request

__all__ = ['fileApp_api']

fileApp_api = Blueprint('fileApp_api',__name__)


@fileApp_api.route('/upload', methods=['POST'])
@login_required
@Request.json('age_type: int', 'wave: int', 'survey_type: int', 'year: int')
def upload_file(age_type, wave, survey_type, year):
    ''' save file'''
    #check if user upload folder exist, or create one
    #user = 'current user' tbd user
    user_file = Upload_Files(current_user.username, age_type, wave, survey_type, year)
    try:
        filename = user_file.get_user_file(request.files['file'])
        if  filename == "No files":
            return HTTPError('No files', 404)
    except:
        return HTTPError('unknown error', 406)
    
    try:
        '''save info to db'''
        user_file.save_file_info(filename)
    except:
        return HTTPError('unknown error db', 406)
    return HTTPResponse('ok')

@fileApp_api.route('/export', methods=['POST'])
@login_required #tbc to be confirmed
@Request.json('merge_method: str', 'file_format: str')
def export_file(merge_method, file_format):
    user_file = Export_Files(current_user.username, merge_method, file_format)
    ''' send file to user'''
    try:
        res = user_file.get_db_file()
        if res == "Could not create merge file":
	        return HTTPError('File can\'t merge', 404)
        res = user_file.export_file_to_user()
        if res == "Fail":
            return HTTPError('Fail to send file', 403)
    except:
        return HTTPError('unknown error', 406)

    return HTTPResponse('ok')