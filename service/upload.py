import os
from werkzeug.utils import secure_filename
from repo.upload.sav import SavUpload, SurveyInfo
from config.config import get_yaml_config


class NoFileError(OSError):
    pass


class FileFormatError(Exception):
    pass


__all__ = ['Upload_Files']

ALLOWED_EXTENSIONS = {'csv', 'sav'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Upload_Files():
    def __init__(self, age_type, wave, survey_type):
        self.age_type = age_type
        self.wave = wave
        self.survey_type = survey_type

    def get_file_folder(self):
        #get user folder path
        UPLOAD_FOLDER = get_yaml_config('upload_dir')
        file_dir = os.path.join(UPLOAD_FOLDER, str(self.age_type),
                                str(self.survey_type))
        #create user folder if not exist
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        return file_dir

    def get_user_file(self, request_file):
        # check if the post request has the file part
        if not request_file:
            raise NoFileError

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if request_file.filename == '':
            raise NoFileError

        #there is file
        if request_file and allowed_file(request_file.filename):
            filename = secure_filename(str(self.wave) + ".sav")
            file_path = os.path.join(self.get_file_folder(), filename)
            request_file.save(file_path)
        else:
            raise FileFormatError

    def save_file_info(self, filename):
        survey_info = SurveyInfo(self.age_type, self.survey_type, self.wave, 1)
        manager = SavUpload()
        manager.upload_sav(filename, survey_info)
