import os
from flask import send_file, Blueprint
from flask_login import current_user
from http import HTTPStatus
from flask_login import login_required
from service.account import Account
from service.upload import Upload_Files
from service.export import Export_Files
from .utils.response import HTTPResponse, HTTPError
from .utils.request import Request
from .utils.auth_required import admin_required

__all__ = ['fileApp_api']

fileApp_api = Blueprint('fileApp_api',__name__)


@fileApp_api.route('/upload', methods=['POST'])
@login_required
@admin_required
@Request.form('file','ageType', 'wave', 'surveyType')
def upload_file(file, ageType, wave, surveyType):
    ''' save file'''
    #check if user upload folder exist, or create one
    #user = 'current user' tbd user
    user_file = Upload_Files(current_user.account_name, ageType, wave, surveyType)
    try:
        filename = user_file.get_user_file(file)
        if  filename == "No files":
            return HTTPError('No files', 404)
        if filename == "Fail":
            return HTTPError('Failed to save file', 405)
    except:
        return HTTPError('unknown error', 406)
    try:
        '''save info to db'''
        user_file.save_file_info(filename)
    except:
        return HTTPError('unknown error db', 406)
    return HTTPResponse('ok')

@fileApp_api.route('/export', methods=['GET'])
@login_required #tbc to be confirmed
@Request.args('mergeMethod', 'fileFormat')
def export_file(mergeMethod, fileFormat):
    user_file = Export_Files(current_user.id, current_user.account_name, mergeMethod, fileFormat)
    ''' send file to user'''
    try:
        res = user_file.get_db_file()
        if res == "Could not create merge file":
	        return HTTPError('File can\'t merge', 404)
        if res == False:
            return HTTPError('DB fail', 405)
        res = user_file.export_file_to_user()
        if res == "Fail":
            return HTTPError('Fail to send file', 403)
    except:
        return HTTPError('unknown error', 406)

    return res
