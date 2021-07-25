import os
from http import HTTPStatus
from database.account import Account
from database.upload import Upload_Files

__all__ = ['fileApp_api']

fileApp_api = Blueprint('fileApp_api',__name__)

fileApp_api.config["UPLOAD_FOLDER"] = '/upload' #tbd upload folder path

ALLOWED_EXTENSIONS = {'csv', 'sav'}

@fileApp_api.route('/upload', methods=['POST'])
def upload_file():
    ''' save file'''
    #check if user upload folder exist, or create one
    user = 'current user' #tbd user
	user_file = Upload_Files(user)
    try:
        filename = user_file.get_file(request)
        if  filename == "No files"
            return {}, HTTPStatus.NOT_FOUND
    except:
        return HTTPStatus.FORBIDDEN
    '''
        save file to db
    '''
    '''
        delete file?
    '''
    return {'file':filename}, HTTPStatus.OK