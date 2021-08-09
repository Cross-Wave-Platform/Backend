from typing import List
from pandas.core.reshape.merge import merge
import pyreadstat
import pandas
import os

# for memory usage
import resource

def merger(file_names: List[str], used_columns: List[List[str]], merge_type: str, file_type: str) -> bool:

    # check file exists
    for item in file_names:
        if os.path.isfile(item) == False:
            print(item)
            return False

    dataframes = []
    metas = []

    for i in range(len(file_names)):
        temp_df, temp_meta = pyreadstat.read_sav(file_names[i], usecols=used_columns[i])# 
        dataframes.append(temp_df)
        metas.append(temp_meta)

    result = pandas.DataFrame()

    if merge_type == 'union':
        result = pandas.concat(dataframes)
    else:
        # how can be ['left','right','outer','inner','cross']
        for i in range(len(dataframes) - 1):
            if i == 0:
                result = pandas.merge( left=dataframes[0], right=dataframes[1], how=merge_type, on=['baby_id'], suffixes=['_M3','_M6'])
            else:
                result = pandas.merge( left=result, right=dataframes[i+1], how=merge_type, on=['baby_id'], suffixes=['_M3','_M6'])


        # result = pandas.merge( left=dataframes[0], right=dataframes[1], how=merge_type, on=['baby_id'], suffixes=['_M3','_M6'])

    for i in dataframes:
        print(i)
    print(result)
    # result.to_csv('testing.csv', index=False)

    return True


if __name__ == "__main__":
    # example
    file_names = ['../KIT3月齡組第1波3月齡家長_final.sav', '../KIT3月齡組第2波6月齡家長_final.sav']# , './KIT3月齡組第1波3月齡親友_final.sav'
    # file_names = [ item for item in file_names for repet in range(10)]
    # print(file_names)
    used_columns = [['baby_id', 'pfa0101', 'pfa0102'], ['baby_id','pfa0201']]

    print( merger(file_names,used_columns,'inner','csv'))

    print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, 'KB')

# file name wll be <big/small>_<type>_<wave>.sav

# time conversion
# bais = 141428 * 86400
# df['baby_dob'] = pandas.to_timedelta( (df['baby_dob'] - bais), unit='s') + pandas.Timestamp('1970-1-1')
# df['int_date'] = pandas.to_timedelta( (df['int_date'] - bais), unit='s') + pandas.Timestamp('1970-1-1')
# print(df)

# print(meta.original_variable_types) # this is for the data type reffered by sav files
# there are other metadata pieces extracted. See the documentation for more details.
# '''
# these values should be given
