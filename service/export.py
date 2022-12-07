import os
import zipfile
from flask import send_file
from config.config import get_yaml_config
from repo.export.merge import MergeManager

__all__ = ['Export_Files']


class SendFail(Exception):
    pass


class CompressError(Exception):
    pass


class Export_Files():
    def __init__(self, id, username, merge_method, file_format, wave):
        self.id = id
        self.username = username
        self.merge_method = merge_method
        self.file_format = file_format
        self.wave = wave
        self.merge_file = None
        self.facet = None

    def get_user_folder(self):
        #get user folder path
        DOWNLOAD_FOLDER = get_yaml_config('download_dir')
        file_dir = os.path.join(DOWNLOAD_FOLDER, self.username)
        #create user folder if not exist
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        return file_dir

    def get_db_file(self):
        ''' get user request info'''
        ''' write info to file'''
        UPLOAD_FOLDER = get_yaml_config('upload_dir')
        '''save file to user export folder'''
        user_download_path = self.get_user_folder()

        manager = MergeManager(self.merge_method, self.file_format, self.wave)
        manager.merger(self.id, UPLOAD_FOLDER, user_download_path)

        if self.file_format == "sav":
            merge_file_path = os.path.join(user_download_path, 'output.sav')
        else:
            merge_file_path = os.path.join(user_download_path, 'output.csv')
            facet_path = os.path.join(user_download_path, 'output.xlsx')
            merge_file_path = self.compress_file([merge_file_path, facet_path])

        self.merge_file = merge_file_path

    def compress_file(self, file_paths):
        merge_file_path = os.path.join(self.get_user_folder(), 'merge.zip')
        try:
            with zipfile.ZipFile(merge_file_path, 'w') as zf:
                for p in file_paths:
                    zf.write(p, os.path.basename(p))
            return merge_file_path
        except Exception as e:
            raise CompressError from e

    def export_file_to_user(self):
        '''send file to user'''
        try:
            return send_file(self.merge_file, as_attachment=True)
        except Exception as e:
            raise SendFail from e
