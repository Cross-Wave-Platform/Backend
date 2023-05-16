import pandas
from .manager import SQLManager


class HistoryManager(SQLManager):
    
    def get_count(self, survey_id: str, startDate: str, endDate: str):
        self.cursor.execute("SELECT COUNT(*) FROM dbo.download_history WHERE survey_id = %s AND download_time >= '%s' AND download_time <= '%s 23:59:59'"% (survey_id, startDate, endDate))
        count = self.cursor.fetchone()[0]
        return count

    def get_list(self):
        command = (
            "SELECT email, age_type, survey_type, wave, download_time "
            "FROM ( "
            "( SELECT account_id, survey_id, download_time FROM dbo.download_history ) AS alpha "
            "INNER JOIN dbo.survey ON alpha.survey_id = survey.survey_id) "
            "INNER JOIN dbo.account ON alpha.account_id = account.account_id;")

        download_history = pandas.read_sql(command, self.conn)

        return download_history
