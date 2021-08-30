import pymssql
from config.config import get_yaml_config


# use config file to connect mssql
class SQLManager:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        config = get_yaml_config('mssql')

        self.conn = pymssql.connect(host=config['host'],
                                    user=config['user'],
                                    password=config['password'],
                                    database=config['database'])
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def __del__(self):
        self.close()

    # dump dataframe to csv, and execute sql bulk insert
    def bulk_insert(self, df, table: str):
        tmp_dir = get_yaml_config('tmp_dir')
        file_name = table.split(".")[1]
        file_path = f'{tmp_dir}/{file_name}.csv'

        df.to_csv(file_path, index=False)
        insert_op = (
            fr"BULK INSERT {table} "
            fr"FROM '{file_path}' "
            fr"WITH ( CHECK_CONSTRAINTS, CODEPAGE='RAW', FIRSTROW=2, FORMAT='CSV');"
        )
        self.cursor.execute(insert_op)
        self.conn.commit()