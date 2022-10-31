from ..manager import SQLManager
import pandas
import pyreadstat
from ..utils import TRANS_ATTRS

def lower_meta(meta):
    res={}
    for org_k,trans_k in TRANS_ATTRS.items():
        attr=getattr(meta,org_k)

        if type(attr)==list:
            res[trans_k] = [l.lower() for l in attr]
        elif type(attr)==dict:
            res[trans_k] = {k.lower():v for k,v in attr.items()}
        else:
            res[trans_k]= attr

    if len(meta.notes):
        res['note']=meta.notes[0]

    return res

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
        res = pandas.read_sql( command, self.engine)
        return res.to_dict('records',dict)

    def upload_sav(self, sav_path: str, survey_info: SurveyInfo):
        
        # force lowercase and resave
        df, meta = pyreadstat.read_sav(sav_path)  
        df.columns= [c.lower() for c in df.columns]
        trans_meta= lower_meta(meta)
        pyreadstat.write_sav(df,sav_path,**trans_meta)
        
        # reload file
        _ , meta = pyreadstat.read_sav(sav_path,metadataonly=True)

        survey_id = self.search_survey(survey_info)

        if survey_info.release:
            open_release_op = (
                "UPDATE dbo.survey SET release=1 WHERE survey_id = %(survey_id)d "
            )

            self.cursor.execute(open_release_op,
                                params={"survey_id": survey_id})

        col_count = self.add_survey_problem(meta, survey_id, survey_info.release)

        return meta.number_rows,col_count

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

        command = ("DELETE FROM survey_problem WHERE survey_id = %(survey_id)s")
        self.cursor.execute(command,{'survey_id':survey_id})
        self.conn.commit()

        survey_problems = pandas.DataFrame()
        survey_problems['problem_name'] = meta.column_names

        problems = pandas.read_sql(
            'SELECT problem_name,problem_id FROM dbo.problem;', self.engine)
        survey_problems = survey_problems.merge(problems,
                                                how='inner',
                                                on='problem_name')

        survey_problems['survey_id'] = survey_id
        survey_problems['release'] = release
        survey_problems = survey_problems[[
            'survey_id', 'problem_id', 'release'
        ]]

        self.bulk_insert(survey_problems, 'dbo.survey_problem')
        return len(survey_problems.index)
