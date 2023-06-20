from .manager import SQLManager
from config.config import get_yaml_config
import pymssql


class AccountSQLManager(SQLManager):
    def __init__(self, asdict=False):
        self.conn = None
        self.cursor = None
        self.connect(asdict)

    def connect(self, asdict):
        config = get_yaml_config('mssql')

        self.conn = pymssql.connect(host=config['host'],
                                    user=config['user'],
                                    password=config['password'],
                                    database=config['database'])
        self.cursor = self.conn.cursor(as_dict=asdict)

    def add_account(self, username: str, hash_in: str, email: str):
        insert_op = 'INSERT INTO dbo.account (account_name,nickname, password, email) VALUES (%(username)s,%(nickname)s, %(email)s, %(password)s)'
        self.cursor.execute(
            insert_op, {
                'username': username,
                'nickname': username,
                'password': hash_in,
                'email': email
            })
        user_id = self.cursor.lastrowid
        self.conn.commit()
        return user_id

    def validate_account(self, user_id: int):
        change_op = 'UPDATE dbo.account SET validated=1 WHERE account_id=%(user_id)s'
        self.cursor.execute(change_op, {
            'user_id': user_id
        })
        self.conn.commit()

    def change_password(self, username: str, hash_new: str):
        change_op = 'UPDATE dbo.account SET password=%(new_password)s WHERE account_name=%(username)s'
        self.cursor.execute(change_op, {
            'username': username,
            'new_password': hash_new
        })
        self.conn.commit()

    def change_nickname(self, username: str, nickname: str):
        change_op = 'UPDATE dbo.account SET nickname=%(nickname)s WHERE account_name=%(username)s'
        self.cursor.execute(change_op, {
            'username': username,
            'nickname': nickname
        })
        self.conn.commit()

    def loadinfo(self, username: str):
        search_op = 'SELECT account_name, nickname, email, auth FROM dbo.account WHERE account_name=%(username)s'
        try:
            self.cursor.execute(search_op, {
                'username': username,
            })
        except:
            return None
        data = self.cursor.fetchone()
        return data

    def get_by_username(self, username: str):
        search_op = 'SELECT * FROM dbo.account WHERE account_name=%(username)s'
        try:
            self.cursor.execute(search_op, {'username': username})
        except:
            return None
        data = self.cursor.fetchone()
        return data

    def get_by_email(self, email: str):
        search_op = 'SELECT * FROM dbo.account WHERE email=%(email)s'
        try:
            self.cursor.execute(search_op, {'email': email})
        except:
            return None
        data = self.cursor.fetchone()
        return data
