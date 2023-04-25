import pandas as pd
import json
from repo.announcement import AnnouncementManager

__all__ = ['Announcement']


class NotEnoughParams(Exception):
    pass


class WrongParamType(Exception):
    pass


class Announcement():

    @classmethod
    def create_announcement(cls, title, contents):

        manager = AnnouncementManager()

        manager.create_announcement(title, contents)

    @classmethod
    def update_announcement(cls, id, title, contents):

        manager = AnnouncementManager()

        manager.update_announcement(id, title, contents)

    @classmethod
    def delete_announcement(cls, id):

        manager = AnnouncementManager()

        manager.delete_announcement(id)

    @classmethod
    def list_announcement(cls):

        manager = AnnouncementManager()

        announcement_list = manager.list_announcement()

        return announcement_list

    @classmethod
    def query_announcement(cls, id):

        manager = AnnouncementManager()

        announcement = manager.query_announcement(id)

        return announcement
