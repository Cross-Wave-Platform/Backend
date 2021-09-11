from mmap import PAGESIZE
from typing import ClassVar
from numpy.core.fromnumeric import product
import pandas
from pandas.core.frame import DataFrame
from ..manager import SQLManager

class SheetCountError(Exception):
    pass

class InvalidName(Exception):
    pass

class MissingSheet(Exception):
    pass

class ColumnNameError(Exception):
    pass

class DataError(Exception):
    pass

class ProblemCollision(Exception):
    pass

class SurveyUpload(SQLManager):
    def upload(self, xlsx_path: str):
        all_data = dict()

        try:
            with open(xlsx_path, 'rb') as file:
                all_data = pandas.read_excel(file, sheet_name=None)
        except IOError as exec:
            raise exec

        # print(all_data)

        # suppose there are three sheets [家長問卷,教保問卷,親友問卷]
        # need to change the code here to have more references
        if len(all_data) != 3:
            raise SheetCountError

        surveys = []
        # get the parent part
        temp = self.get_survey('家長問卷', all_data)
        surveys.append(temp)

        # get the friend part
        temp = self.get_survey('親友問卷', all_data)
        surveys.append(temp)

        # # get the teacher part
        temp = self.get_survey('教保問卷', all_data)
        surveys.append(temp)

        # flatten
        surveys = [i for sublist in surveys for i in sublist]
        # make it a dataframe
        surveys = pandas.DataFrame(
            surveys, columns=['age_type', 'survey_type', 'wave', 'release'])
        # get the current surveys
        command = ("SELECT * FROM survey;")
        current_survey = pandas.read_sql(command, self.conn)

        # remove duplicates
        surveys = pandas.concat([
            surveys, current_survey[['age_type', 'survey_type', 'wave']]
        ]).drop_duplicates(subset=['age_type', 'survey_type', 'wave'],
                           keep=False)
        surveys['survey_id'] = ''
        surveys = surveys[[
            'survey_id', 'age_type', 'survey_type', 'wave', 'release'
        ]]
        # print(surveys)
        # insert to database
        self.bulk_insert(surveys, 'dbo.survey')

        # get all classes
        # get the current classes
        command = ("SELECT * FROM class;")
        current_class = pandas.read_sql(command, self.conn)

        classes = pandas.DataFrame(columns=['class', 'subclass'])

        classes = classes.append(self.get_class('家長問卷', all_data))
        classes = classes.append(self.get_class('親友問卷', all_data))
        classes = classes.append(self.get_class('教保問卷', all_data))
        # drop duplicates
        classes.drop_duplicates(subset=['class', 'subclass'], inplace=True)
        classes.fillna('', inplace=True)
        classes = pandas.concat([
            classes, current_class[['class', 'subclass']]
        ]).drop_duplicates(subset=['class', 'subclass'],
                           keep=False).reset_index(drop=True)
        # drop no_group
        classes.drop(classes[classes['class'] == 'no_group'].index,
                     inplace=True)
        classes['class_id'] = ''
        classes = classes[['class_id', 'class', 'subclass']]
        # print(classes)
        # insert ot database
        self.bulk_insert(classes, 'dbo.class')
        # get the current classes
        command = ("SELECT * FROM class;")
        current_class = pandas.read_sql(command, self.conn)

        # get all problems
        # get the current problems
        command = ("SELECT * FROM problem;")
        current_problem = pandas.read_sql(command, self.conn)

        problems = pandas.DataFrame(
            columns=['problem_name', 'topic', 'class', 'subclass'])

        problems = problems.append(self.get_problem('家長問卷', all_data))
        problems = problems.append( self.get_problem('親友問卷', all_data))
        problems = problems.append( self.get_problem('教保問卷', all_data))
        problems = problems.reset_index(drop=True)

        problems.drop_duplicates(inplace=True)
        problems['problem_name'] = problems['problem_name'].str.lower()
        problems = pandas.merge(left=problems,
                                right=current_class,
                                on=['class', 'subclass'])

        # remove duplicate from current
        problems = pandas.concat([
            problems, current_problem[['problem_name', 'topic', 'class_id']]
        ]).drop_duplicates(subset=['problem_name', 'topic', 'class_id'],
                           keep=False)

        # check for same problem_name but different other things
        # sanity check
        sanity = problems.groupby('problem_name').size().to_list()
        if sanity and max(sanity) != 1:
            raise ProblemCollision

        # give it problem_id and sort the columns
        problems['problem_id'] = ''
        problems = problems[[
            'problem_id', 'problem_name', 'topic', 'class_id'
        ]]
        print(problems)
        # insert to database
        self.bulk_insert(problems, 'dbo.problem')

        # get survey_problem
        # this will be handled by the sav upload part

        return 'success'

    def get_survey(self, sheet_name: str, all_data: dict):
        # check the sheet name and set survey_type
        survey_type = 0
        if sheet_name == '教保問卷':
            survey_type = 1
        elif sheet_name == '家長問卷':
            survey_type = 2
        elif sheet_name == '親友問卷':
            survey_type = 3
        else:
            raise InvalidName

        # get the page
        page = all_data.get(sheet_name, "not_found")
        if type(page) == str and page == "not_found":
            raise MissingSheet

        # pandas.DataFrame(columns=['age_type','survey_type','wave','release'])
        # convert to dataframe later
        survey = []

        # print( page.columns.to_list()[4:])

        for string in page.columns.to_list()[4:]:
            age_type = string.split('月齡組')[0]
            if age_type == '3':
                age_type = 1
            elif age_type == '36':
                age_type = 2
            elif 'Unnamed' in age_type:
                raise DataError
            else:
                raise ColumnNameError

            # need to restrict this kind of usage
            wave = string.split('\n')[1]

            survey.append([age_type, survey_type, wave])

        for i in range(len(survey)):
            release = ''
            survey[i].append(release)

        return survey

    def get_class(self, sheet_name: str, all_data: dict):
        page = all_data.get(sheet_name)

        classes = page[['主構面', '次構面']].rename(columns={
            '主構面': 'class',
            '次構面': 'subclass'
        }).drop_duplicates()

        # the duplicates will be delt at the main function
        # classes = classes.append(database_class[['class', 'subclass']]).drop_duplicates(keep=False)

        classes.dropna(subset=['class'], inplace=True)

        return classes

    def get_problem(self, sheet_name: str, all_data: dict):

        page = all_data.get(sheet_name)

        problems = page[['變項名稱', '變項標籤', '主構面', '次構面']].rename(
            columns={
                '變項名稱': 'problem_name',
                '變項標籤': 'topic',
                '主構面': 'class',
                '次構面': 'subclass'
            })

        problems.dropna(subset=['problem_name'], inplace=True)
        problems.fillna('',inplace=True)

        return problems

    def get_survey_problem(self, sheet_name: str, all_data: dict):
        page = all_data.get(sheet_name)
        survey_list = self.get_survey(sheet_name, all_data)

        survey_problem = pandas.DataFrame(columns=[
            'age_type', 'survey_type', 'wave', 'release', 'problem_name'
        ])

        for i in range(len(survey_list)):
            temp = page.iloc[:, [0, i + 4]]
            temp = temp[temp.iloc[:, 1] == 'O']
            temp = temp.rename(columns={'變項名稱': 'problem_name'})
            # print(temp)

            temp['age_type'] = survey_list[i][0]
            temp['survey_type'] = survey_list[i][1]
            temp['wave'] = survey_list[i][2]
            temp['release'] = survey_list[i][3]

            temp = temp[[
                'age_type', 'survey_type', 'wave', 'release', 'problem_name'
            ]]
            survey_problem = survey_problem.append(temp)

        # print(survey_problem)
        return survey_problem
