import pandas as pd
import json
from repo.picture import PictureManager

__all__ = ['Picture']


class NotEnoughParams(Exception):
    pass


class WrongParamType(Exception):
    pass


class Picture():

    @classmethod
    def input_picture(cls, id , picture):

        manager = PictureManager()

        manager.input_picture(id,picture)

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

        manager = PictureManager()

        picture_list = manager.list_picture()

        return picture_list

