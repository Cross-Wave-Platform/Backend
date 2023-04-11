import pandas
from .manager import SQLManager


class HistoryManager(SQLManager):
    
    def get_count(self, survey_id: str, startDate: str, endDate: str):
        self.cursor.execute("SELECT COUNT(*) FROM dbo.download_history WHERE survey_id = %s AND download_time >= '%s' AND download_time <= '%s 23:59:59'"% (survey_id, startDate, endDate))
        count = self.cursor.fetchone()[0]
        return count
