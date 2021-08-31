from flask import Blueprint
from flask_login import current_user, login_required

from .utils.response import HTTPResponse, HTTPError
from .utils.request import Request
from .utils.auth_required import AuthLevel, auth_required
from service.account import Account

__all__ = ['personalApp_api']

personalApp_api = Blueprint('personalApp_api', __name__)


@personalApp_api.route('/changepassword', methods=['PUT'])
@login_required
@auth_required(AuthLevel.REGULAR)
@Request.json('oldPassword: str', 'newPassword: str')
def change_password(oldPassword, newPassword):
    try:
        current_user.change_password(oldPassword, newPassword)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('change password success')
