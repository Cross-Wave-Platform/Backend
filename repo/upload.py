from .manager import SQLManager
import pandas
import pyreadstat

class SurveyInfo:
    def __init__(self,age_type:int,survey_type:int,wave:int):
        self.age_type= age_type
        self.survey_type = survey_type
        self.wave =wave

class UploadManager(SQLManager):
    def upload_sav(self,sav_path:str,survey_info:SurveyInfo):
        _,meta = pyreadstat.read_sav(sav_path,metadataonly=True)

        new_id = self.add_survey(survey_info)

        if not new_id:
            print ('already exists')
        else:
            self.add_problems(meta,new_id)
            print ('success')


    # survey_id is auto_increment without give the value
    # check duplicate, if not, return survey_id it gets
    def add_survey(self,survey_info:SurveyInfo):
        check_dupl_op = ('SELECT survey_id,age_type, survey_type, wave FROM survey '
                         'WHERE age_type=%(age_type)d AND survey_type=%(survey_type)d AND wave=%(wave)d;')
        params = {'age_type':survey_info.age_type,
                  'survey_type':survey_info.survey_type,
                  'wave':survey_info.wave}

        old_survey = pandas.read_sql(check_dupl_op,self.conn,params=params)

        if not old_survey.empty:
            return

        command = ('INSERT INTO survey ( age_type, survey_type, wave) '
                   'VALUES(%(age_type)d,%(survey_type)d,''%(wave)d);')
        self.cursor.execute(command,params)
        self.conn.commit()

        command = "SELECT max( survey_id) FROM survey;"
        self.cursor.execute(command)
        row = self.cursor.fetchone()

        survey_id = row[0]
        return survey_id

    def add_problems(self,meta,survey_id):

        given_problems = pandas.DataFrame()
        given_problems['problem_id'] = ''
        given_problems['problem_name'] = meta.column_names
        given_problems['topic'] = meta.column_labels
        given_problems['survey_id'] =survey_id
        given_problems['class'] =''
        given_problems['subclass'] =''

        self.bulk_insert( given_problems, 'dbo.problems')
