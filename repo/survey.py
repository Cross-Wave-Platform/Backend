
from mmap import PAGESIZE
from typing import ClassVar
from numpy.core.fromnumeric import product
import pandas
from pandas.core.frame import DataFrame
from .manager import SQLManager

# what is '3月齡組\n18月齡（已回補）', does '（已回補）' have meaning??

class SurveyUpload(SQLManager):
    def upload( self, xlsx_path: str):
        all_data = dict()

        try:
            with open(xlsx_path, 'rb') as file:
                all_data = pandas.read_excel(file,sheet_name=None)
        except IOError as exec:
            return exec.strerror

        # print(all_data)

        # suppose there are three sheets [家長問卷,教保問卷,親友問卷]
        # need to change the code here to have more references
        if len(all_data) != 3:
            return 'sheet_count_error'

        surveys = []
        # get the parent part
        # this is not usable since the file format is not settled
        temp = self.get_survey('家長問卷',all_data)
        if type(temp) == str:
            return temp
        surveys.append(temp)

        # get the friend part
        temp = self.get_survey('親友問卷',all_data)
        if type(temp) == str:
            return temp
        surveys.append(temp)

        # # get the teacher part
        temp = self.get_survey('教保問卷',all_data)
        if type(temp) == str:
            return temp
        surveys.append(temp)

        # flatten
        surveys = [ i for sublist in surveys for i in sublist]
        # make it a dataframe
        surveys = pandas.DataFrame(surveys, columns=['age_type','survey_type','wave','release'])
        # get the current surveys
        command = ("SELECT * FROM survey;")
        current_survey = pandas.read_sql(command,self.conn)

        # remove duplicates
        surveys = pandas.concat([surveys, current_survey[['age_type','survey_type','wave','release']]]).drop_duplicates(subset=['age_type','survey_type','wave','release'], keep=False)
        surveys['survey_id'] = ''
        surveys = surveys[['survey_id','age_type','survey_type','wave','release']]
        print(surveys)


        # get all classes
        # get the current classes
        command = ("SELECT * FROM class;")
        current_class = pandas.read_sql( command, self.conn)
        # print(current_class)

        classes = pandas.DataFrame(columns=['class','subclass'])

        classes = classes.append( self.get_class('家長問卷', all_data))
        classes = classes.append( self.get_class('親友問卷', all_data))
        classes = classes.append( self.get_class('教保問卷', all_data))
        # drop duplicates
        classes = pandas.concat([classes, current_class[['class','subclass']]]).drop_duplicates(subset=['class', 'subclass'],keep=False)
        # drop no_group
        classes.drop( classes[classes['class'] == 'no_group'].index, inplace=True)
        classes['class_id'] = ''
        classes = classes[['class_id','class','subclass']]
        print( classes)


        # get all problems
        # get the current problems
        command = ("SELECT * FROM problem;")
        current_problem = pandas.read_sql( command, self.conn)

        problems = pandas.DataFrame(columns=['problem_name','topic','class','subclass'])

        problems = problems.append( self.get_problem('家長問卷', all_data))
        # problems = problems.append( self.get_problem('親友問卷', all_data))
        # problems = problems.append( self.get_problem('教保問卷', all_data))

        problems.drop_duplicates(inplace=True)
        problems = pandas.merge( left=problems, right=current_class, on=['class','subclass'])

        # remove duplicate from current
        problems = pandas.concat([problems,current_problem[['problem_name','topic','class_id']]]).drop_duplicates(subset=['problem_name','topic','class_id'],keep=False)

        # check for same problem_name but different other things

        # give it problem_id and sort the columns
        problems['problem_id'] = ''
        problems = problems[['problem_id','problem_name','topic','class_id']]
        print(problems)


        # get survey_problem
        survey_problems = self.get_survey_problem('家長問卷', all_data)

        survey_problems = pandas.merge(left=survey_problems, right=current_problem, on=['problem_name'])
        survey_problems = pandas.merge(left=survey_problems, right=current_survey, on=['age_type','survey_type','wave','release'])

        survey_problems = survey_problems[['survey_id','problem_id']]
        # remove duplicates
        command = ("SELECT * FROM survey_problem;")
        current_survey_problem = pandas.read_sql(command,self.conn)

        survey_problems = pandas.concat([survey_problems,current_survey_problem[['survey_id','problem_id']]]).drop_duplicates(subset=['survey_id','problem_id'],keep=False)
        survey_problems['release'] = '1'
        print(survey_problems)


        # insert all data to database
        self.bulk_insert( surveys, 'dbo.survey')
        self.bulk_insert( classes, 'dbo.class')
        self.bulk_insert( problems, 'dbo.problem')
        self.bulk_insert( survey_problems, 'dbo.survey_problem')

        return 'success'

    # need to tweek the numbers of columns that need to be chooped off
    def get_survey( self, sheet_name: str, all_data: dict):
        # check the sheet name and set survey_type
        survey_type = 0
        if sheet_name == '教保問卷':
            survey_type = 1
        elif sheet_name == '家長問卷':
            survey_type = 2
        elif sheet_name == '親友問卷':
            survey_type = 3
        else:
            return sheet_name + '_invalid_name'

        # get the page
        page = all_data.get(sheet_name, "not_found")
        if type(page) == str and page == "not_found":
            return sheet_name + '_missing'
        
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
                print(age_type)
                return 'unexpected_data_error'
            else:
                print(age_type)
                return '月齡組_error'
            
            # this is a full sized '('
            # need to restrict this kind of usage
            wave = string.split('\n')[1].split('（')[0]
            
            survey.append([age_type,survey_type,wave])
        
        # the release part
        release_row = [ i for sublist in page.iloc[-1:].values.tolist() for i in sublist]
        # slice the unused columns
        release_row = release_row[4:]

        # print(survey,release_row)

        for i in range(len(survey)):
            release = 0
            if release_row[ i] == '已釋出':
                release = 1
            
            survey[ i].append(release)

        return survey

    # there seems to be duplicate '不等機率加權值' and are not being shed off
    def get_class( self, sheet_name: str, all_data: dict):
        page = all_data.get( sheet_name)

        classes = page[['主構面','次構面']].rename(columns={'主構面':'class','次構面':'subclass'}).drop_duplicates()

        # the duplicates will be delt at the main function
        # classes = classes.append(database_class[['class', 'subclass']]).drop_duplicates(keep=False)

        classes.dropna(inplace=True)

        return classes

    def get_problem( self, sheet_name: str, all_data: dict):

        page = all_data.get(sheet_name)

        problems = page[['變項名稱','變項標籤','主構面','次構面']].rename(columns={'變項名稱':'problem_name','變項標籤':'topic','主構面':'class','次構面':'subclass'})

        problems.dropna(subset=['problem_name'], inplace=True)

        # print(problems)

        return problems

    def get_survey_problem( self, sheet_name: str, all_data: dict):
        page = all_data.get(sheet_name)
        survey_list = self.get_survey( sheet_name, all_data)

        survey_problem = pandas.DataFrame(columns=['age_type','survey_type','wave','release','problem_name'])

        for i in range(len(survey_list)):
            temp = page.iloc[:,[0,i+4]]
            temp = temp[temp.iloc[:,1] == 'O']
            temp = temp.rename(columns={'變項名稱':'problem_name'})
            # print(temp)

            temp['age_type'] = survey_list[ i][ 0]
            temp['survey_type'] = survey_list[ i][ 1]
            temp['wave'] = survey_list[ i][ 2]
            temp['release'] = survey_list[ i][ 3]

            temp = temp[['age_type','survey_type','wave','release','problem_name']]
            survey_problem = survey_problem.append(temp)
            
        # print(survey_problem)
        return survey_problem
