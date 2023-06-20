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
    def create_announcement(cls, title, contents, pinned):

        manager = AnnouncementManager()

        manager.create_announcement(title, contents, pinned)

    @classmethod
    def update_announcement(cls, id, title, contents, pinned):

        manager = AnnouncementManager()

        manager.update_announcement(id, title, contents, pinned)

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
