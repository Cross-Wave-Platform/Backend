import os
import pandas as pd
import pyreadstat as prs
from .config import UPLOAD_FOLDER
from werkzeug.utils import secure_filename

__all__ = ['Upload_Files']

UPLOAD_FOLDER = '/upload'
DOWNLOAD_FOLDER = '/download' 
ALLOWED_EXTENSIONS = {'csv', 'sav'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class Upload_Files():
    def __init__(self, username, age_type, wave, survey_type, year):
        self.username = username
        self.age_type = age_type
        self.wave = wave
        self.survey_type = survey_type
        self.year = year

    def get_file_folder(self):
        #get user folder path
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
        if request_file.filename == '':
            return "No files"
        
        #there is file
        if request_file and allowed_file(request_file.filename):
            filename = secure_filename(self.wave+self.year)
            file_path = os.path.join(self.get_file_folder(), filename)
            request_file.save(file_path)
        return file_path