
from typing import List
from pandas.core.reshape.merge import merge
import pyreadstat
import pandas
import os
from functools import reduce

from .manager import SQLManager

# for memory usage
import resource

class MergeManeger( SQLManager):
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
                suffix.append('_'+('small' if str(row['age_type']) == 1 else 'big')+'_'+temp_survey+'_M'+str(row['wave']))
                used_columns.append(['baby_id'])
            
            used_columns[ file_names.index(temp_path)].append(row['problem_name'])

        # print(file_names)
        # print(used_columns)
        # print(suffix)

        temp_columns = []

        for i in used_columns:
            for item in i:
                if item != 'baby_id':
                    temp_columns.append(item)
        
        dup_columns = []

        for i in temp_columns:
            if temp_columns.count(i) > 1:
                dup_columns.append(i)
        
        dup_columns = list(set(dup_columns))

        # print(temp_columns)
        # print(dup_columns)

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
            dataframes.append(temp_df)
            metas.append(temp_meta)

        # print(dataframes)

        result = pandas.DataFrame()

        if merge_method == 'union':
            result = pandas.concat(dataframes)
        else:
            # add the suffixes to the dataframes
            # this needs more fixing AKA some columns do not need the suffix maybe rstrip the suffix?
            # for i in range(len(dataframes)):
            #     dataframes[ i] = dataframes[i].add_suffix(suffix[ i])
            
            # print(dataframes[0].get('baby_id'))

            # how can be ['left','right','outer','inner','cross']
            result = reduce( lambda left, right: pandas.merge( left, right, on=['baby_id'], how=merge_method), dataframes)

            print(result.columns)
        # return True
        if file_format == 'sav':
            # important metas
            # column_name == problem_name
            # column_labels == topic
            # variable_value_labels == {problem_name:{num:'characters'}}

            # if variable_measure has a collision => set to 'unknown'
            # this will maybe be implemented later
            # get the union of all the variable_measure
            # variable_measure_union = set()
            # for i in metas:
            #     variable_measure_union = variable_measure_union | metas[i].variable_measure

            # if variable_value_labels does not match => union them
            # need dict union
            full_dict = dict()

            for i in range( len(metas)):
                # print(metas[i].variable_value_labels)
                full_dict.update(metas[i].variable_value_labels)

            # print(full_dict)


            # get column_labels AKA topic
            # get union of the problems
            problem_union = []
            for i in metas:
                problem_union.append(i.column_names)
            # flatten list
            problem_union = [ item for sublist in problem_union for item in sublist]
            # drop duplicates
            problem_union = list(set(problem_union))
            problem_union = pandas.DataFrame( problem_union, columns=['problem_name'])

            command = "SELECT problem_name, topic FROM problem;"
            problem_topics = pandas.read_sql( command,self.conn)
            problem_topics = pandas.merge( left=problem_topics, right=problem_union, how='inner', on=['problem_name'])

            # not in use file_label, compress, note, missing_ranges,variable_display_width( not important), variable_formats( automatic resolve since there is only string and double in the original file)
            pyreadstat.write_sav( result, destination, column_labels=problem_topics['topic'],variable_value_labels=full_dict)#,variable_measure=)
        elif file_format == 'csv':
            # time convertion needed for formats in SDATE10
            for item in metas:
                if item.column_names:
                    return False
        else:
            # not possible
            return False

        return True


# if __name__ == "__main__":
#     # example
#     file_names = ['../KIT3月齡組第1波3月齡家長_final.sav', '../KIT3月齡組第2波6月齡家長_final.sav']
#     # file_names = [ item for item in file_names for repet in range(10)]
#     # print(file_names)
#     used_columns = [['baby_id', 'pfa0101', 'pfa0102'], ['baby_id','pfa0201']]

#     print( merger(file_names,used_columns,'inner','csv'))

#     print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, 'KB')

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
