from flask import Blueprint
from flask_login import current_user
from flask_login import login_required
from service.upload import Upload_Files, FileFormatError, NoFileError, Upload_Problem, get_file_wave, NotEnoughParams
from service.export import Export_Files, SendFail, CompressError
from repo.export.format import FormatTypeError
from repo.export.method import MethodTypeError
from repo.export.merge import SurveyNotFound
from .utils.response import HTTPResponse, HTTPError
from .utils.request import Request
from .utils.auth_required import auth_required, AuthLevel
from repo.upload.sav import SurveyNotExists

__all__ = ['fileApp_api']

fileApp_api = Blueprint('fileApp_api', __name__)


@fileApp_api.route('/upload/sav', methods=['POST'])
@login_required
@auth_required(AuthLevel.ADMIN)
@Request.files('file')
@Request.form('ageType', 'wave', 'surveyType')
def upload_file(file, ageType, wave, surveyType):
    ''' save file'''

    #check if user upload folder exist, or create one
    #user = 'current user' tbd user
    try:
        user_file = Upload_Files(ageType, wave, surveyType)
        filename = user_file.get_user_file(file)
    except NotEnoughParams:
        return HTTPError('Not enough params', 403)
    except NoFileError:
        return HTTPError('No files', 404)
    except FileFormatError:
        return HTTPError('File format error', 405)
    except:
        return HTTPError('unknown error', 406)

    try:
        '''save info to db'''
        user_file.save_file_info(filename)
    except SurveyNotExists:
        user_file.remove_failed_file(filename)
        return HTTPError('survey not exists', 403)
    except:
        user_file.remove_failed_file(filename)
        return HTTPError('unknown error db', 406)
    return HTTPResponse('successfully uploaded')


@fileApp_api.route('/upload/surveyProblem', methods=['POST'])
@login_required
@auth_required(AuthLevel.ADMIN)
@Request.files('file')
def upload_problem(file):
    ''' save file'''

    #check if user upload folder exist, or create one
    #user = 'current user' tbd user
    user_file = Upload_Problem()
    try:
        filename = user_file.get_user_file(file)
    except NoFileError:
        return HTTPError('No files', 404)
    except FileFormatError:
        return HTTPError('File format error', 405)
    except:
        return HTTPError('unknown error', 406)

    try:
        '''save info to db'''
        user_file.save_file_info(filename)
    # except SurveyNotExists:
    #     return HTTPError('survey not exists', 403)
    except:
        return HTTPError('unknown error db', 406)
    return HTTPResponse('successfully uploaded')

@fileApp_api.route('/fileWave', methods=['GET'])
@login_required
@auth_required(AuthLevel.ADMIN)
def file_wave():
    try: 
        wave = get_file_wave()
    except:
        return HTTPError('Unkown error', 406)
    return HTTPResponse('ok', data={"wave":wave})


@fileApp_api.route('/export', methods=['GET'])
@login_required  #tbc to be confirmed
@auth_required(AuthLevel.REGULAR)
@Request.args('mergeMethod', 'fileFormat')
def export_file(mergeMethod, fileFormat):
    user_file = Export_Files(current_user.id, current_user.account_name,
                             mergeMethod, fileFormat)
    ''' send file to user'''
    try:
        user_file.get_db_file()
        res = user_file.export_file_to_user()
    except (MethodTypeError, FormatTypeError):
        return HTTPError('Wrong type of merge method or format', 403)
    except SurveyNotFound:
        return HTTPError('Select survey not found', 404)
    except CompressError:
        return HTTPError('Compress fail', 405)
    except SendFail:
        return HTTPError('Fail to send file', 406)
    except:
        return HTTPError('unknown error', 406)

    return res
