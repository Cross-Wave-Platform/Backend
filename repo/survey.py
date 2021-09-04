
from numpy.core.fromnumeric import product
import pandas
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
        # temp = self.get_survey('家長問卷',all_data)
        # if type(temp) == str:
        #     return temp
        # surveys.append(temp)

        # get the friend part
        temp = self.get_survey('親友問卷',all_data)
        if type(temp) == str:
            return temp
        surveys.append(temp)

        # get the teacher part
        temp = self.get_survey('教保問卷',all_data)
        if type(temp) == str:
            return temp
        surveys.append(temp)

        # flatten
        surveys = [ i for sublist in surveys for i in sublist]

        surveys = pandas.DataFrame(surveys, columns=['age_type','survey_type','wave','release'])

        print(surveys)






        # insert all data to database
        # self.bulk_insert(surveys, 'dbo.survey')

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

        # print( page.columns.to_list()[3:])

        for string in page.columns.to_list()[3:]:
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
            
            wave = string.split('\n')[1].split('月齡')[0]
            try:
                wave = int(wave)
            except ValueError:
                return 'column_name_error'
            
            survey.append([age_type,survey_type,wave])
        
        # the release part
        release_row = [ i for sublist in page.iloc[-1:].values.tolist() for i in sublist]
        # slice the unused columns
        release_row = release_row[3:]

        # print(survey,release_row)

        for i in range(len(survey)):
            release = 0
            if release_row[ i] == '已釋出':
                release = 1
            
            survey[ i].append(release)

        return survey
