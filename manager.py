import yaml
from yaml import CLoader as Loader
import pkgutil
import pymssql

class SQLManager:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        config_data = pkgutil.get_data(__package__,'config.yaml')
        config = yaml.load(config_data,Loader)['mssql']

        self.conn = pymssql.connect(
                        host= config['host'],
                        user= config['user'],
                        password= config['password'],
                        database= config['database']
                    )
        self.cursor=self.conn.cursor()
                    
    def close(self):
        self.cursor.close()
        self.conn.close()
    
    def __del__(self):
        self.close()
