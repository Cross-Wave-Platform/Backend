import os
import pandas
import datetime
from flask import send_file
from config.config import get_yaml_config
from repo.history import HistoryManager

__all__ = ['History']


class NotEnoughParams(Exception):
    pass


class WrongParamType(Exception):
    pass


class SendFail(Exception):
    pass



class History():

    @classmethod
    def get_count(cls, survey_id, startDate, endDate):

        manager = HistoryManager()

        count = manager.get_count(survey_id, startDate, endDate)

        return count


class Export_History():
    def __init__(self, username):
        self.username = username
        self.history_file = None

    def get_user_folder(self):
        #get user folder path
        DOWNLOAD_FOLDER = get_yaml_config('download_dir')
        file_dir = os.path.join(DOWNLOAD_FOLDER, self.username)
        #create user folder if not exist
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        return file_dir

    def get_db_file(self):
        '''save file to user export folder'''
        user_download_path = self.get_user_folder()

        manager = HistoryManager()

        history_list = manager.get_list()

        current_time = datetime.datetime.now()
        str_time = current_time.strftime("%Y%m%d%H%M%S")

        file_path = os.path.join(user_download_path, str_time + '_history.xlsx')

        with pandas.ExcelWriter(file_path) as writer:
            history_list.to_excel(writer,
                                sheet_name='download_history',
                                index=False)

        self.history_file = file_path

    def export_file_to_user(self):
        '''send file to user'''
        try:
            return send_file(self.history_file, as_attachment=True)
        except Exception as e:
            raise SendFail from e
