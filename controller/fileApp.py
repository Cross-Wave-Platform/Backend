from flask import Blueprint
from flask_login import current_user
from flask_login import login_required
from service.upload import Upload_Files, FileFormatError, NoFileError
from service.export import Export_Files, CantMerge, SendFail
from .utils.response import HTTPResponse, HTTPError
from .utils.request import Request
from .utils.auth_required import auth_required, AuthLevel
from repo.upload.sav import SurveyNotExists

__all__ = ['fileApp_api']

fileApp_api = Blueprint('fileApp_api', __name__)


@fileApp_api.route('/upload', methods=['POST'])
@login_required
@auth_required(AuthLevel.ADMIN)
@Request.files('file')
@Request.form('ageType', 'wave', 'surveyType')
def upload_file(file, ageType, wave, surveyType):
    ''' save file'''

    #check if user upload folder exist, or create one
    #user = 'current user' tbd user
    user_file = Upload_Files(ageType, wave, surveyType)
    try:
        filename = user_file.get_user_file(file)
    except NoFileError:
        return HTTPError('No files', 404)
    except FileFormatError:
        return HTTPError('Failed to save file', 405)
    except:
        return HTTPError('unknown error', 406)

    try:
        '''save info to db'''
        user_file.save_file_info(filename)
    except SurveyNotExists:
        return HTTPError('survey not exists', 403)
    except:
        return HTTPError('unknown error db', 406)
    return HTTPResponse('ok')


@fileApp_api.route('/export', methods=['GET'])
@login_required  #tbc to be confirmed
@auth_required(AuthLevel.REGULAR)
@Request.args('mergeMethod', 'fileFormat')
def export_file(mergeMethod, fileFormat):
    user_file = Export_Files(current_user.id, current_user.account_name,
                             mergeMethod, fileFormat)
    ''' send file to user'''
    try:
        res = user_file.get_db_file()
        if res == False:
            return HTTPError('DB fail', 405)
        res = user_file.export_file_to_user()
    except CantMerge:
        return HTTPError('File can\'t merge', 404)
    except SendFail:
        return HTTPError('Fail to send file', 403)
    except:
        return HTTPError('unknown error', 406)

    return res
