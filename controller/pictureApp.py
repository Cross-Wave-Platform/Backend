from flask import Blueprint
from flask_login import current_user, login_required
from service.picture import NotEnoughParams, Picture, WrongParamType
from .utils.response import HTTPResponse, HTTPError
from .utils.request import Request
from .utils.auth_required import AuthLevel, auth_required

__all__ = ['pictureApp_api']

pictureApp_api = Blueprint('pictureApp_api', __name__)

@pictureApp_api.route('/inputPicture', methods=['POST'])
@login_required
@auth_required(AuthLevel.ADMIN)
@Request.files('picture')
@Request.form('id')
def input_picture(id,picture):
    try:
        Picture.input_picture(id,picture)
    except NotEnoughParams:
        return HTTPError('Not enough params', 405)
    except WrongParamType:
        return HTTPError('Wrong Param Type', 405)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('input picture success')


@pictureApp_api.route('/updatePicture', methods=['PUT'])
@login_required
@auth_required(AuthLevel.ADMIN)
@Request.files('picture')
@Request.form('id:int')
def update_picture(id, picture):
    try:
        Picture.update_picture(id, picture)
    except NotEnoughParams:
        return HTTPError('Not enough params', 405)
    except WrongParamType:
        return HTTPError('Wrong Param Type', 405)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('update picture success')


@pictureApp_api.route('/deletePicture', methods=['DELETE'])
@login_required
@auth_required(AuthLevel.ADMIN)
@Request.json('id')
def delete_picture(id):
    try:
        Picture.delete_picture(id)
    except NotEnoughParams:
        return HTTPError('Not enough params', 405)
    except WrongParamType:
        return HTTPError('Wrong Param Type', 405)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('delete picture success')


@pictureApp_api.route('/listPicture', methods=['GET'])
def list_picture():
    try:
        picture_list = Picture.list_picture()
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('list picture success', data=picture_list)
