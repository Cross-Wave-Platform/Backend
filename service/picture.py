import os
import pandas as pd
from werkzeug.utils import secure_filename
import base64
import json
from flask import send_file
from config.config import get_yaml_config

__all__ = ['Picture']


class NotEnoughParams(Exception):
    pass


class WrongParamType(Exception):
    pass


class Picture():

    @classmethod
    def input_picture(cls, id , picture):

        UPLOAD_FOLDER = get_yaml_config('upload_dir')
        filename = secure_filename(id + ".jpg")
        file_path = os.path.join(UPLOAD_FOLDER, 'picture' , filename)
        picture.save(file_path)

    @classmethod
    def delete_picture(cls, id):

        UPLOAD_FOLDER = get_yaml_config('upload_dir')
        filename = secure_filename(str(id) + ".jpg")
        file_path = os.path.join(UPLOAD_FOLDER, 'picture' , filename)
        os.remove(file_path)

    @classmethod
    def list_picture(cls):

        UPLOAD_FOLDER = get_yaml_config('upload_dir')
        picture_list = []

        for i in range(1,5):
            filename = secure_filename(str(i) + ".jpg")
            file_path = os.path.join(UPLOAD_FOLDER, 'picture',filename)
            if(os.path.exists(file_path)): 
                with open(file_path, 'rb') as f:
                    imageData = f.read()
                    base64Data = base64.b64encode(imageData)
                    base64Data = base64Data.decode('utf-8')
                    picture_list.append(base64Data)

        return picture_list

