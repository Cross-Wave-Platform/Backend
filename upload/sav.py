from numpy import isnan
from numpy.lib.function_base import copy, insert
from yaml import error
from .operation import bulk_insert
import pandas

def add_problems(manager, meta):
    old_problems = pandas.read_sql( 'SELECT problem_id FROM dbo.problems;', manager.conn)

    given_problems = pandas.DataFrame()
    given_problems['problem_id'] = meta.column_names
    given_problems['topic'] = meta.column_labels
    given_problems['class'] = ''

    insert_problems = pandas.concat([given_problems,old_problems]).drop_duplicates(subset='problem_id',keep=False)

    bulk_insert(manager, insert_problems, 'dbo.tag_value')

def add_tag_values(manager, meta):
    dict_list = []

    for problem_id, pairs in meta.variable_value_labels.items():
        for tag_value, tag_name in pairs.items():
            row_data = {'problem_id': problem_id,
                        'tag_value': int(float(tag_value)),
                        'tag_name': tag_name}
            dict_list.append(row_data)
    tag_values = pandas.DataFrame.from_records(dict_list)

    bulk_insert(manager, tag_values, 'dbo.tag_value')


# todo: get survey_id
def add_survey_problems(manager, meta):
    survey_id = 1

    survey_problems = pandas.DataFrame()

    survey_problems['problems'] = meta.column_names
    survey_problems['survey_id'] = survey_id
    column_names = ['survey_id', 'problems']

    survey_problems = survey_problems.loc[:, column_names]
    bulk_insert(manager, survey_problems, 'dbo.survey_problem')


# todo: get survey_id, start_answer_id
def add_answers(manager, df, meta):
    start_answer_id = 1
    survey_id = 1
    # generating answers table
    answers = pandas.DataFrame()

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

    bulk_insert(manager,answers,'dbo.answer')
