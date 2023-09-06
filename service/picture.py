import os
import pandas as pd
from werkzeug.utils import secure_filename
import base64
import json
from flask import send_file
from repo.picture import PictureManager
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
    def update_picture(cls, id, picture):

        manager = PictureManager()

        manager.update_picture(id, picture)

    @classmethod
    def delete_picture(cls, id):

        manager = PictureManager()

        manager.delete_picture(id)

    @classmethod
    def list_picture(cls):

        UPLOAD_FOLDER = get_yaml_config('upload_dir')
        file_path = os.path.join(UPLOAD_FOLDER, 'picture', '1.jpg')
        picture_list = []

        with open(file_path, 'rb') as f:
            imageData = f.read()
            base64Data = base64.b64encode(imageData)
            base64Data = base64Data.decode('utf-8')
            picture_list.append(base64Data)

        return picture_list

