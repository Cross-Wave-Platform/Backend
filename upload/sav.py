from ..manager import SQLManager
import pyreadstat as prs
import yaml
from yaml import CLoader as Loader
import pandas as pd
import pkgutil

def bulk_insert(manager,df,table):
    config_data = pkgutil.get_data('Database','config.yaml')
    tmp_dir =  yaml.load(config_data,Loader)['tmp_dir']
    file_name = table.split(".")[1]
    file_path = f'{tmp_dir}/{file_name}.csv'

    df.to_csv(file_path,index=False)
    bulk_insert_op = fr'''BULK INSERT {table}
                          FROM '{file_path}' 
                          WITH ( CODEPAGE='RAW', FIRSTROW=2, FORMAT='CSV');'''
    manager.cursor.execute(bulk_insert_op)
    manager.conn.commit()

def add_tag_value(meta):
    dict_list=[]

    for problem_id, pairs in  meta.variable_value_labels.items():
        for tag_value, tag_name in pairs.items():
            row_data = {'problem_id':problem_id,
                        'tag_value':int(float(tag_value)),
                        'tag_name':tag_name}
            dict_list.append(row_data)
    df = pd.DataFrame.from_records(dict_list)

    manager = SQLManager()
    bulk_insert(manager,df,'dbo.tag_value')
