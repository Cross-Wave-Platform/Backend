from flask import Blueprint
from flask_login import current_user, login_required

from .utils.response import HTTPResponse, HTTPError
from .utils.request import Request
from .utils.auth_required import AuthLevel, auth_required

__all__ = ['personal_api']

personal_api = Blueprint('personal_api', __name__)


@personal_api.route('/changepassword', methods=['PUT'])
@login_required
@auth_required(AuthLevel.REGULAR)
@Request.json('old_password: str', 'new_password: str')
def change_password(old_password, new_password):
    try:
        current_user.change_password(old_password, new_password)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('change password success')
