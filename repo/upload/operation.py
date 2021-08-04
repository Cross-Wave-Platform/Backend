import yaml
from yaml import CLoader as Loader
import pkgutil

# dump dataframe to csv, and execute sql bulk insert
def bulk_insert(manager, df, table):
    config_data = pkgutil.get_data('Backend.repo', 'config.yaml')
    tmp_dir = yaml.load(config_data, Loader)['tmp_dir']
    file_name = table.split(".")[1]
    file_path = f'{tmp_dir}/{file_name}.csv'

    df.to_csv(file_path, index=False)
    bulk_insert_op = (fr"BULK INSERT {table} "
                      fr"FROM '{file_path}' " 
                      fr"WITH ( CHECK_CONSTRAINTS, CODEPAGE='RAW', FIRSTROW=2, FORMAT='CSV');")
    manager.cursor.execute(bulk_insert_op)
    manager.conn.commit()
