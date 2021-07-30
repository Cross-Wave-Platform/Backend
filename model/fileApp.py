import os
from flask import request, send_file
from http import HTTPStatus
from db-module.account import Account
from db-module.upload import Upload_Files
from db-module.export import Export_Files

__all__ = ['fileApp_api']

fileApp_api = Blueprint('fileApp_api',__name__)

fileApp_api.config["UPLOAD_FOLDER"] = '/upload' #tbd upload folder path
fileApp_api.config["DOWNLOAD_FOLDER"] = '/download' #tbd download folder path

ALLOWED_EXTENSIONS = {'csv', 'sav'}

@fileApp_api.route('/upload', methods=['POST'])
@login_required
def upload_file():
    ''' save file'''
    #check if user upload folder exist, or create one
    user = 'current user' #tbd user
	user_file = Upload_Files(user)
    try:
        filename = user_file.get_user_file(request.file)
        if  filename == "No files"
            return {}, HTTPStatus.NOT_FOUND
    except:
        return {}, HTTPStatus.FORBIDDEN
    '''
        save file to db
    '''
    '''
        delete file?
    '''
    return {'file':filename}, HTTPStatus.OK

@fileApp_api.route('/export', methods=['POST'])
@login_required #tbc to be confirmed
def export_file():
    ''' get user request info'''

    ''' write info to file'''

    ''' send file to user'''
    user = 'current user' #tbd get current user
    user_file = Export_Files(user, request.json['merge_method'], request.json['file_format'])
    try:
        res = user_file.get_db_file()
        if res == "Could not create merge file":
	        return {}, HTTPStatus.NOT_FOUND
        res = user_file.export_file_to_user()
        if res == "Fail":
            return {}, HTTPStatus.Fail
    except:
        return {}, HTTPStatus.FORBIDDEN