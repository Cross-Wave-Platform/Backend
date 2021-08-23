from .manager import SQLManager
import pandas
import pyreadstat

class SurveyInfo:
    def __init__(self, age_type: int, survey_type: int, wave: int,release:int):
        self.age_type = age_type
        self.survey_type = survey_type
        self.wave = wave
        self.release = release


class UploadManager(SQLManager):
    def upload_sav(self, sav_path: str, survey_info: SurveyInfo):
        _, meta = pyreadstat.read_sav(sav_path, metadataonly=True)
        # force lowercase
        meta.column_names = list(map(lambda p: p.lower(), meta.column_names))

        new_id = self.add_survey(survey_info)

        if not new_id:
            print('already exists')
        else:
            self.add_problem(meta)
            self.add_survey_problem(meta,new_id,survey_info.release)
            print('success')

    # survey_id is auto_increment without give the value
    # check duplicate, if not, return survey_id it gets
    def add_survey(self, survey_info: SurveyInfo):
        check_dupl_op = ('SELECT survey_id,age_type, survey_type, wave FROM survey '
                         'WHERE age_type=%(age_type)d AND survey_type=%(survey_type)d AND wave=%(wave)d;')
        params = {'age_type': survey_info.age_type,
                  'survey_type': survey_info.survey_type,
                  'wave': survey_info.wave}

        old_survey = pandas.read_sql(check_dupl_op, self.conn, params=params)

        if not old_survey.empty:
            return

        command = ('INSERT INTO survey ( age_type, survey_type, wave,release) '
                   'VALUES(%(age_type)d,%(survey_type)d,%(wave)d,%(release)d);')
        params['release'] = survey_info.release
        self.cursor.execute(command, params)
        self.conn.commit()

        command = "SELECT max( survey_id) FROM survey;"
        self.cursor.execute(command)
        row = self.cursor.fetchone()

        survey_id = row[0]
        return survey_id

    def add_problem(self, meta):
        old_problems = pandas.read_sql( 'SELECT problem_name FROM dbo.problem;', self.conn)

        given_problems = pandas.DataFrame()
        given_problems['problem_id'] = ''
        given_problems['problem_name'] = meta.column_names
        given_problems['topic'] = meta.column_labels
        given_problems['class'] = ''

        insert_problems = pandas.concat([given_problems,old_problems]).drop_duplicates(subset='problem_name',keep=False)

        if not insert_problems.empty:
            self.bulk_insert(insert_problems, 'dbo.problem')

    def add_survey_problem(self, meta,survey_id:int,release:int):
        
        survey_problems = pandas.DataFrame()
        survey_problems['problem_name'] = meta.column_names

        problems = pandas.read_sql('SELECT problem_name,problem_id FROM dbo.problem;',self.conn)
        survey_problems = survey_problems.merge(problems,how='inner',on='problem_name')

        survey_problems['survey_id'] = survey_id
        survey_problems['release'] = release
        survey_problems = survey_problems[['survey_id','problem_id','release']]
        
        self.bulk_insert( survey_problems, 'dbo.survey_problem')