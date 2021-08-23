import os
import zipfile
import pandas as pd
import pyreadstat as prs
from flask import send_file
from .utils import get_yaml_config
from repo.merging import MergeManeger

__all__ = ['Export_Files']

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
        DOWNLOAD_FOLDER = get_yaml_config()['download_dir']
        file_dir = os.path.join( DOWNLOAD_FOLDER , self.username)
        print(file_dir)
        #create user folder if not exist
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        return file_dir
    
    def get_db_file(self):
        ''' get user request info'''
        ''' write info to file'''
        UPLOAD_FOLDER = get_yaml_config()['upload_dir']
        merge_file_path = os.path.join(self.get_user_folder(), 'output.sav')
        self.merge_file = merge_file_path
        try:
            # save export file
            print("START??????")
            manager = MergeManeger()
            manager.merger(self.id, UPLOAD_FOLDER, self.get_user_folder(), self.merge_method, self.file_format)
        except:
            return "Could not create merge file"
        return "Success"

    def compress_file(self):
        merge_file_path = os.path.join(self.get_user_folder(), 'merge.zip')
        try:
            with zipfile.ZipFile(merge_file_path, 'w') as zf:
                zf.write(self.merge_file)
                zf.write(self.facet)
        except:
            return "Fail to compress merge file"
        return "Success"

    def export_file_to_user(self):
        '''send file to user'''
        try:
            send_file(self.merge_file, as_attachment=True, attachment_filename="output.sav")
            print(self.merge_file)
        except:
            return "Fail to send file"
        return send_file(self.merge_file, as_attachment=True, attachment_filename="output.sav")