import os
import zipfile
import pandas as pd
import pyreadstat as prs
from .config import DOWNLOAD_FOLDER
from flask import send_file

__all__ = ['Export_Files']

class Export_Files():
    def __init__(self, username, merge_method, file_format):
        self.username = username
        self.merge_method = merge_method
        self.file_format = file_format
        self.merge_file = None
        self.facet = None

    def get_user_folder(self):
        #get user folder path  
        file_dir = os.path.join( DOWNLOAD_FOLDER , self.username)
        #create user folder if not exist
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        return file_dir
    
    def get_db_file(self):
        ''' get user request info'''
        ''' write info to file'''
        '''
        get request info from db
        df = pd.DataFrame([["a", 1],[2.2, 2],[3.3, "b"]], columns=['Var1', 'Var2'])
        variable_value_labels = {'Var1':{'a':'a missing value'}
        missing_ranges = {'Var1':['a'], 'Var2': ['b']}
        formats = {'val1':'N4', 'val2':'F1.0'}
        variable_format=formats, missing_ranges=missing_ranges, variable_value_labels=variable_value_labels
        '''
        df = 'retrieved data' #tbd data from db, df in pandas dataframe structurre

        '''save file to user export folder'''
        merge_file_path = os.path.join(self.get_user_folder(), 'merge.sav')
        try:
            prs.write_sav(df, merge_file_path)
        except:
            return "Could not create merge file"
        self.merge_file = merge_file_path
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
            send_file(self.merge_file, as_attachment=True,attachment_filename='merge_file')
        except:
            return "Fail to send file"
        return "Success"