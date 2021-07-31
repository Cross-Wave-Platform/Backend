from .operation import bulk_insert
from ..manager import SQLManager
import pandas
import pyreadstat

class SurveyInfo:
    def __init__(self,age_type,survey_type,wave):
        self.age_type= age_type
        self.survey_type = survey_type
        self.wave =wave

def upload_sav(sav_path,survey_info):
    df , meta = pyreadstat.read_sav(sav_path,formats_as_category=True)
    manager= SQLManager()

    survey_id = add_survey(manager,survey_info)

    if survey_id:
        add_problems(manager,meta)
        add_tag_values(manager,meta)
        add_survey_problems(manager,survey_id,meta)
        add_answers(manager,survey_id,df,meta)
        print('success')
    else:
        print('duplicate survey')



# survey_id is auto_increment without give the value
# return survey_id it gets
def add_survey(manager, survey_info):
    command = f'SELECT age_type, survey_type, wave FROM survey;'

    old_surveys = pandas.read_sql(command,manager.conn)

    new_surveys = pandas.DataFrame()

    new_surveys['age_type'] = survey_info.age_type
    new_surveys['survey_type'] = survey_info.survey_type
    new_surveys['wave'] = survey_info.wave

    dup = pandas.merge(left=old_surveys,right=new_surveys)

    if not dup.empty:
        return None

    command = (f'INSERT INTO survey ( age_type, survey_type, wave) '
               f'VALUES({survey_info.age_type},{survey_info.survey_type},'
                      f'{survey_info.wave});')
    manager.cursor.execute(command)
    manager.conn.commit()

    command = "SELECT max( survey_id) FROM survey;"
    manager.cursor.execute(command)
    row = manager.cursor.fetchone()

    survey_id = row[0]
    return survey_id

def add_problems(manager, meta):
    old_problems = pandas.read_sql( 'SELECT problem_id FROM dbo.problems;', manager.conn)

    given_problems = pandas.DataFrame()
    given_problems['problem_id'] = meta.column_names
    given_problems['topic'] = meta.column_labels
    given_problems['class'] = ''

    insert_problems = pandas.concat([given_problems,old_problems]).drop_duplicates(subset='problem_id',keep=False)

    if not insert_problems.empty:
        bulk_insert(manager, insert_problems, 'dbo.problems')

# create tag_value df from meta,
# drop duplicate data and bulk insert
def add_tag_values(manager, meta):
    
    dict_list = []
    for problem_id, pairs in meta.variable_value_labels.items():
        for tag_value, tag_name in pairs.items():
            row_data = {'problem_id': problem_id,
                        'tag_value': float(tag_value),
                        'tag_name': tag_name}
            dict_list.append(row_data)
    given_tag_values = pandas.DataFrame.from_records(dict_list)

    old_tag_values = pandas.read_sql( 'SELECT problem_id,tag_value FROM dbo.tag_values;', manager.conn)
    insert_tag_value = ( pandas.concat([given_tag_values,old_tag_values]) 
                               .drop_duplicates(subset=['problem_id','tag_value'],keep=False) )

    insert_tag_value=insert_tag_value.convert_dtypes()

    if not insert_tag_value.empty:
        bulk_insert(manager, insert_tag_value, 'dbo.tag_values')


def add_survey_problems(manager,survey_id, meta):

    survey_problems = pandas.DataFrame()

    survey_problems['problems'] = meta.column_names
    survey_problems['survey_id'] = survey_id
    column_names = ['survey_id', 'problems']

    survey_problems = survey_problems.loc[:, column_names]

    survey_problems = survey_problems.convert_dtypes()

    bulk_insert(manager, survey_problems, 'dbo.survey_problems')


def add_answers(manager,survey_id, df, meta):
    # compute new answer_id
    command = "SELECT max( answer_id) FROM answers;"
    manager.cursor.execute(command)
    old_max = manager.cursor.fetchone()[0]
    old_max = old_max if old_max else 0
    start_answer_id = old_max +1

    # generating answers table
    answers = pandas.DataFrame()

    command = f'SELECT answer FROM dbo.answers WHERE problem_id = \'baby_id\';'

    old_baby_id = pandas.read_sql( command, manager.conn)

    old_baby_id = old_baby_id.rename(columns={'answer':'baby_id'})

    df = pandas.concat([df,old_baby_id]).drop_duplicates(subset=['baby_id'], keep=False)

    (answer_count, problem_count) = df.shape

    #force convert float dtype
    df=df.convert_dtypes()
    # this has the columns ['variable', 'value'] in position
    answers = df.T.melt().rename(columns={'variable':'answer_id', 'value':'answer'})

    answers['survey_id'] = survey_id

    answers['problem_id'] = meta.column_names*answer_count

    column_names = ['answer_id', 'problem_id', 'survey_id', 'answer']

    answers = answers.loc[:, column_names]

    answers['answer_id'] = answers['answer_id'] + start_answer_id

    bulk_insert(manager,answers,'dbo.answers')
