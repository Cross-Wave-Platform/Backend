import pandas as pd
import json
from repo.history import HistoryManager

__all__ = ['History']


class NotEnoughParams(Exception):
    pass


class WrongParamType(Exception):
    pass


class History():

    @classmethod
    def get_count(cls, survey_id, startDate, endDate):

        manager = HistoryManager()

        count = manager.get_count(survey_id, startDate, endDate)

        return count
