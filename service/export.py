import os
import zipfile
from flask import send_file
from config.config import get_yaml_config
from repo.merging import MergeManager

__all__ = ['Export_Files']


class CantMerge(Exception):
    pass


class SendFail(Exception):
    pass


class CompressFail(Exception):
    pass


class Export_Files():
    def __init__(self, id, username, merge_method, file_format):
        self.id = id
        self.username = username
        self.merge_method = merge_method
        self.file_format = file_format
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
        merge_file_path = self.get_user_folder()
        try:
            manager = MergeManager()
            res = manager.merger(self.id, UPLOAD_FOLDER, merge_file_path,
                                 self.merge_method, self.file_format)
        except Exception as e:
            raise CantMerge from e
        if self.file_format == "sav":
            merge_file_path = os.path.join(merge_file_path, 'output.sav')
        else:
            merge_file_path = os.path.join(merge_file_path, 'output.xlsx')
        self.merge_file = merge_file_path
        return res

    def compress_file(self):
        merge_file_path = os.path.join(self.get_user_folder(), 'merge.zip')
        try:
            with zipfile.ZipFile(merge_file_path, 'w') as zf:
                zf.write(self.merge_file)
                zf.write(self.facet)
        except Exception as e:
            raise CompressFail from e

    def export_file_to_user(self):
        '''send file to user'''
        try:
            send_file(self.merge_file, as_attachment=True)
        except Exception as e:
            raise SendFail from e
        return send_file(self.merge_file, as_attachment=True)
