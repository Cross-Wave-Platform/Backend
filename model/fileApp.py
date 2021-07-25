import os
import pandas as pd
import pyreadstat as prs
from flask import Flask, Blueprint, request
from werkzeug.utils import secure_filename
from http import HTTPStatus
from database.account import Account

__all__ = ['fileApp_api']

fileApp_api = Blueprint('fileApp_api',__name__)

fileApp_api.config["UPLOAD_FOLDER"] = '/upload' #tbd upload folder path

ALLOWED_EXTENSIONS = {'csv', 'sav'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@fileApp_api.route('/upload', methods=['POST'])
def upload_file():
    ''' save file'''
    #check if user upload folder exist, or create one
    user = 'current user' #tbd user
	file_dir = os.path.join(fileApp_api.config['UPLOAD_FOLDER'] , user["account"]) #tbd user['account']
	if not os.path.exists(file_dir):
		os.makedirs(file_dir)
    try:
        # check if the post request has the file part
        if 'file' not in request.files:
            return {}, HTTPStatus.NOT_FOUND #tbd or other status code
        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return {}, HTTPStatus.NOT_FOUND
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(file_dir, filename))
    except:
        return HTTPStatus.FORBIDDEN
    '''
        save file to db
    '''
    '''
        delete file?
    '''
    return {'file':filename}, HTTPStatus.OK