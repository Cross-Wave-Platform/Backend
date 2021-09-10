from ..manager import SQLManager
import pandas
import pyreadstat


class SurveyNotExists(Exception):
    pass


class SurveyInfo:
    def __init__(self, age_type: int, survey_type: int, wave: str,
                 release: int):
        self.age_type = age_type
        self.survey_type = survey_type
        self.wave = wave
        self.release = release


class SavUpload(SQLManager):
    def search_all_survey(self):
        command = "SELECT survey_id, age_type, survey_type, wave FROM survey;"
        res = pandas.read_sql( command, self.conn)
        return res.to_dict('records',dict)

    def upload_sav(self, sav_path: str, survey_info: SurveyInfo):
        _, meta = pyreadstat.read_sav(sav_path, metadataonly=True)
        # force lowercase
        meta.column_names = list(map(lambda p: p.lower(), meta.column_names))

        survey_id = self.search_survey(survey_info)

        if survey_info.release:
            open_release_op = (
                "UPDATE dbo.survey SET release=1 WHERE survey_id = %(survey_id)d "
            )

            self.cursor.execute(open_release_op,
                                params={"survey_id": survey_id})

        self.add_survey_problem(meta, survey_id, survey_info.release)

    def search_survey(self, survey_info):
        search_op = (
            "SELECT survey_id FROM dbo.survey "
            "WHERE age_type=%(age_type)d AND survey_type=%(survey_type)d AND wave=%(wave)s "
        )

        self.cursor.execute(search_op,
                            params={
                                "age_type": survey_info.age_type,
                                "survey_type": survey_info.survey_type,
                                "wave": survey_info.wave
                            })

        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            raise SurveyNotExists

    def add_survey_problem(self, meta, survey_id: int, release: int):

        survey_problems = pandas.DataFrame()
        survey_problems['problem_name'] = meta.column_names

        problems = pandas.read_sql(
            'SELECT problem_name,problem_id FROM dbo.problem;', self.conn)
        survey_problems = survey_problems.merge(problems,
                                                how='inner',
                                                on='problem_name')

        survey_problems['survey_id'] = survey_id
        survey_problems['release'] = release
        survey_problems = survey_problems[[
            'survey_id', 'problem_id', 'release'
        ]]

        self.bulk_insert(survey_problems, 'dbo.survey_problem')
