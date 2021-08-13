from .manager import SQLManager


class SearchManager(SQLManager):
    def search_waves(self, age_type, survey_type):
        search_op = ("SELECT wave "
                     "FROM dbo.survey "
                     "WHERE age_type = %(age_type)s "
                     "AND survey_type = %(survey_type)s "
                     "AND release = 1")
        params = {'age_type': age_type, 'survey_type': survey_type}

        result = self.cursor.execute(search_op, params)
        return result.fetchall()
