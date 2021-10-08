from flask import Blueprint, request
from flask_login import current_user
from flask_login import login_required
from service.report import Send_Email
from .utils.response import HTTPResponse, HTTPError
from .utils.request import Request
from datetime import datetime
from config.config import get_yaml_config

__all__ = ['reportApp_api']

reportApp_api = Blueprint('reportApp_api', __name__)

admin_email = get_yaml_config('receiver') ##TBC

@reportApp_api.route('/quickReport', methods=['POST'])
@login_required
@Request.form('title', 'content')
def upload_file(title, content):
    if not title:
        title = "No title"
    if not content:
        content = "No content"
    mymail = Send_Email(title+datetime.now().strftime(' %Y/%m/%d %H:%M:%S'),[admin_email])
    try:
        mymail.htmladd(content)
        mymail.addattach(request.files.getlist('file'))   
        mymail.send()
    except Exception as e:
        return HTTPError(str(e), 406) 
    
    return HTTPResponse('successfully send')