
# from typing import List
from numpy.core.numeric import full
from pandas.core.reshape.merge import merge
import pyreadstat
import pandas
import os
from functools import reduce
from .manager import SQLManager

# for memory usage
import resource

class MergeManager( SQLManager):
    def merger(self, account_id: int, upload_path: str, destination: str, merge_method: str, file_format: str) -> bool:
        # get shop_cart info
        command = ("SELECT age_type, survey_type, wave, problem.problem_name "
                    "FROM ( "
                        "( SELECT survey_id, problem_id FROM dbo.shop_cart WHERE account_id = %(account_id)s) AS alpha "
                        "INNER JOIN dbo.survey ON alpha.survey_id = survey.survey_id) "
                    "INNER JOIN dbo.problem ON alpha.problem_id = problem.problem_id;")
        
        shop_cart_survey_problems = pandas.read_sql(command, self.conn, params={'account_id':account_id})

        file_names = []
        used_columns = []
        suffix = []

        for index, row in shop_cart_survey_problems.iterrows():
            temp_path = upload_path +'/'+ str(row['age_type'])+'/'+str(row['survey_type'])+'/'+str(row['wave']) +'.sav'
            if temp_path not in file_names:
                file_names.append(temp_path)
                temp_survey = ''
                if row['survey_type'] == 1:
                    temp_survey = 'teacher'
                elif row['survey_type'] == 2:
                    temp_survey = 'parent'
                elif row['survey_type'] == 3:
                    temp_survey = 'friend'
                suffix.append(('small' if str(row['age_type']) == 1 else 'big')+'_'+temp_survey+'_M'+str(row['wave']))
                used_columns.append(['baby_id'])
            
            used_columns[ file_names.index(temp_path)].append(row['problem_name'])

        # drop duplicate 'baby_id'
        for i in range(len(used_columns)):
            if used_columns[ i][ 1] == 'baby_id':
                used_columns[ i].pop(1)

        # remove dup_columns if not used
        dup_columns = []

        for i in used_columns:
            for item in i:
                if item != 'baby_id':
                    dup_columns.append(item)

        dup_columns = list(set(dup_columns))

        # check file exists
        for item in file_names:
            if os.path.isfile(item) == False:
                print(item)
                return False

        dataframes = []
        metas = []

        for i in range(len(file_names)):
            # need to read the whole file to get the metadata
            temp_df, temp_meta = pyreadstat.read_sav(file_names[i])
            dataframes.append(temp_df.loc[:,used_columns[i]])
            metas.append(temp_meta)

        result = pandas.DataFrame()

        if merge_method == 'union':
            # don't change the suffix
            # add wave column
            for i in range(len(dataframes)):
                dataframes[ i].insert(1,'wave', suffix[ i])
                # kill suffixes for the variable_value_label
                suffix[i] = ''

            result = pandas.concat(dataframes)
        else:
            # add suffix to columns other than 'baby_id'
            for i in range(len(dataframes)):
                dataframes[ i] = dataframes[ i].add_suffix('_'+suffix[i])
                dataframes[ i] = dataframes[ i].rename( columns={ dataframes[ i].columns[ 0] : 'baby_id'})
            # how can be ['left','right','outer','inner','cross']
            result = reduce( lambda left, right: pandas.merge( left, right, on=['baby_id'], how=merge_method), dataframes)

        # if variable_value_labels does not match => union them
        # need dict union
        full_dict = dict()

        for columns in range(len( used_columns)):
            for item in range(len( used_columns[columns])):
                column_name = used_columns[columns][ item]
                if column_name == 'baby_id':
                    full_dict.update({'baby_id':metas[columns].variable_value_labels.get('baby_id')})
                elif column_name not in full_dict:
                    if merge_method == 'union':
                        full_dict.update({column_name:metas[columns].variable_value_labels.get(column_name)})
                    else:
                        full_dict.update({column_name+'_'+suffix[columns]:metas[columns].variable_value_labels.get(column_name)})
                else:
                    # need to union
                    inside = full_dict.get( column_name)
                    inside.update( metas[columns].variable_value_labels.get(column_name))
                    full_dict.update({column_name:inside})

        # filter the values that are 'None'
        filtered = { k : v for k, v in full_dict.items() if v is not None}
        full_dict.clear()
        full_dict.update( filtered)

        # get column_labels AKA topic
        # get union of the problems
        problem_union = used_columns.copy()
        # flatten list
        problem_union = [ item for sublist in problem_union for item in sublist]
        # drop duplicates
        problem_union = list(set(problem_union))
        problem_union = pandas.DataFrame( problem_union, columns=['problem_name'])

        command = "SELECT problem_name, topic FROM problem;"
        problem_topics = pandas.read_sql( command,self.conn)
        problem_topics = pandas.merge( left=problem_topics, right=problem_union, how='inner', on=['problem_name'])
        column_labels = problem_topics['topic'].tolist()
        if merge_method == 'union':
            column_labels.insert(1,'wave_in_chinese')
        
        if file_format == 'sav':
            destination += '/output.sav'
            # important metas
            # column_names == problem_name
            # column_labels == topic
            # variable_value_labels == {problem_name:{num:'characters'}}

            # if variable_measure has a collision => set to 'unknown'
            # this will maybe be implemented later
            # get the union of all the variable_measure
            # variable_measure_union = set()
            # for i in metas:
            #     variable_measure_union = variable_measure_union | metas[i].variable_measure

            # not in use file_label, compress, note, missing_ranges,variable_display_width( not important), variable_formats( automatic resolve since there is only string and double in the original file)
            pyreadstat.write_sav( result, destination, column_labels= column_labels,variable_value_labels=full_dict)#,variable_measure=)
        elif file_format == 'xlsx':
            destination += '/output.xlsx'
            # time convertion needed for formats in SDATE10
            bais = 141428 * 86400
            for file in range(len(used_columns)):
                for column in range(len(used_columns[ file])):
                    original_type = metas[ file].original_variable_types.get(used_columns[ file][column])
                    if "DATE" in original_type:
                        # time conversion and get the date only
                        current_column = used_columns[ file][column]
                        if merge_method != 'union':
                            current_column = current_column+'_'+suffix[file]
                        result[current_column] = pandas.to_timedelta( (result[current_column] - bais), unit='s') + pandas.Timestamp('1970-1-1')
                        result[current_column] = result[current_column].dt.date

            # get the ( problem_id,  problem_name, variable_value_labels)
            problem_value_labels = pandas.DataFrame()
            problem_value_labels['problem_id'] = result.columns
            # add the topic
            if merge_method != 'union':
                for file in range(len(used_columns)):
                    for col in range(len(used_columns[file])):
                        before = used_columns[file][col]
                        current_column = used_columns[file][col]
                        if current_column != 'baby_id':
                            current_column  = current_column+'_'+suffix[file]
                        problem_value_labels.loc[ problem_value_labels['problem_id'] == current_column,'topic'] = problem_topics.loc[ problem_topics['problem_name'] == before,'topic']
            else:
                problem_value_labels['topic'] = column_labels
            
            # add the value_label
            for item in result.columns:
                problem_value_labels.loc[problem_value_labels['problem_id'] == item,'variable_value_label'] = str(full_dict.get(item))
            
            with pandas.ExcelWriter(destination, datetime_format="YYYY-MM-DD") as writer:
                result.to_excel( writer, index= False, sheet_name='Data')
                problem_value_labels.to_excel( writer, index= False, sheet_name='Value_Labels')
        else:
            # not possible
            return False

        return True


# file name will be <big/small>/<type>/<wave>.sav
# all metadata consists of the following
# 20 -> ['notes'empty,'column_names','column_labels','column_names_to_labels','file_encoding'BIG-5,
#       'number_columns','number_rows','variable_value_labels','value_labels','variable_to_label',
#       'original_variable_types','readstat_variable_types','table_name','file_label','missing_ranges',
#       'missing_user_values','variable_alignement','variable_store_width','variable_display_width','variable_measure']

# time conversion
# bais = 141428 * 86400
# df['baby_dob'] = pandas.to_timedelta( (df['baby_dob'] - bais), unit='s') + pandas.Timestamp('1970-1-1')
# df['int_date'] = pandas.to_timedelta( (df['int_date'] - bais), unit='s') + pandas.Timestamp('1970-1-1')
# print(df)
