from flask import Blueprint
from flask_login import current_user, login_required
from service.announcement import NotEnoughParams, Announcement, WrongParamType
from .utils.response import HTTPResponse, HTTPError
from .utils.request import Request
from .utils.auth_required import AuthLevel, auth_required

__all__ = ['announcementApp_api']

announcementApp_api = Blueprint('announcementApp_api', __name__)


@announcementApp_api.route('/updateAnnouncement', methods=['PUT'])
@login_required
@auth_required(AuthLevel.ADMIN)
@Request.json('id: int', 'title: str', 'contents: str')
def update_announcement(id, title, contents):
    try:
        Announcement.update_announcement(id, title, contents)
    except NotEnoughParams:
        return HTTPError('Not enough params', 405)
    except WrongParamType:
        return HTTPError('Wrong Param Type', 405)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('update announcement success')


@announcementApp_api.route('/createAnnouncement', methods=['POST'])
@login_required
@auth_required(AuthLevel.ADMIN)
@Request.json('title: str', 'contents: str')
def create_announcement(title, contents):
    try:
        Announcement.create_announcement(title, contents)
    except NotEnoughParams:
        return HTTPError('Not enough params', 405)
    except WrongParamType:
        return HTTPError('Wrong Param Type', 405)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('create announcement success')


@announcementApp_api.route('/deleteAnnouncement', methods=['DELETE'])
@login_required
@auth_required(AuthLevel.ADMIN)
@Request.json('id: int')
def delete_announcement(id):
    try:
        Announcement.delete_announcement(id)
    except NotEnoughParams:
        return HTTPError('Not enough params', 405)
    except WrongParamType:
        return HTTPError('Wrong Param Type', 405)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('delete announcement success')


@announcementApp_api.route('/listAnnouncement', methods=['GET'])
def list_announcement():
    try:
        announcement_list = Announcement.list_announcement()
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('list announcement success', data=announcement_list)


@announcementApp_api.route('/queryAnnouncement', methods=['GET'])
@Request.args('id')
def query_announcement(id):
    try:
        announcement = Announcement.query_announcement(id)
    except NotEnoughParams:
        return HTTPError('Not enough params', 405)
    except WrongParamType:
        return HTTPError('Wrong Param Type', 405)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('query announcement success', data=announcement)