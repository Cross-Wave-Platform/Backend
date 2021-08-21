import os
import base64
import pandas as pd
import pyreadstat as prs
from werkzeug.utils import secure_filename
from repo.upload import UploadManager,SurveyInfo
from .utils import get_yaml_config

__all__ = ['Upload_Files']

ALLOWED_EXTENSIONS = {'csv', 'sav'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def isBase64(s):
    try:
        return base64.b64encode(base64.b64decode(s)) == s
    except Exception:
        return False

def decode_file(file, filename):
    try:
        with open(filename, "wb") as fh:
            fh.write(base64.b64decode(file))
    except:
        return "Fail"
    return "Success"

class Upload_Files():
    def __init__(self, username, age_type, wave, survey_type, year):
        self.username = username
        self.age_type = age_type
        self.wave = wave
        self.survey_type = survey_type
        self.year = year

    def get_file_folder(self):
        #get user folder path
        UPLOAD_FOLDER = get_yaml_config()['upload_dir']
        file_dir = os.path.join( UPLOAD_FOLDER , self.age_type, self.survey_type)
        #create user folder if not exist
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        return file_dir

    def get_user_file(self, request_file):
        # check if the post request has the file part
        if not request_file:
            return "No files"

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if request_file == '':
            return "No files"
        
        #there is file
        if request_file and isBase64(request_file):
            filename = secure_filename(self.wave+".sav")
            file_path = os.path.join(self.get_file_folder(), filename)
            # request_file.save(file_path)
            res = decode_file(request_file, file_path)
        return res

    def save_file_info(self, filename):
        survey_info = SurveyInfo(self.age_type, self.survey_type, self.wave)
        manager = UploadManager()
        manager.upload_sav(filename,survey_info)