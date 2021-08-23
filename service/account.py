from datetime import datetime, timedelta
from .utils import hash_id
from hmac import compare_digest
import pymssql
from repo.manager import SQLManager
from flask_login import UserMixin

import os
import re

__all__ = ['Account']

class Account(UserMixin):
    def __init__(self, account_name, password, email):
        self.account_name = account_name
        self.password = password
        self.email = email

    def get_id(self):
        return self.id

    @classmethod
    def signup(cls, username, password, email):
        if re.match(r'^[a-zA-Z0-9_\-]+$', username) is None:
            raise ValueError

        user = cls.get_by_email(email)
        if user:
            return 'email used'
        user = cls.get_by_username(username)
        if user:
            return 'account exists'
        
        user_id = hash_id(username, password)

        a = SQLManager()
        sql = "INSERT INTO dbo.account (account_name, email, password) VALUES ( \'" + username + "\', \'" + email + "\', \'" + user_id + "\')"
        a.cursor.execute(sql)
        a.conn.commit()
        a.close()
        return 'ok'

    @classmethod
    def login(cls, username, password):
        try:
            user = cls.get_by_username(username)
        except:
            user = cls.get_by_email(username)
        if user is None:
            return 'user not found'

        account = Account(account_name = user[1], password = user[3], email = user[2])
        account.id = username
        user_id = hash_id(account.account_name, password)
        if compare_digest(account.password, user_id):
            return account
        else:
            return 'password incorrect'

    def change_password(self, old_password, new_password):
        user_id = hash_id(self.account_name, old_password)
        if compare_digest(self.password, user_id):
            user_id = hash_id(self.account_name, new_password)
            a = SQLManager()
            sql = "UPDATE dbo.account SET password = \'" + user_id + "\' WHERE account_name = \'" + self.account_name + "\'"
            a.cursor.execute(sql)
            a.conn.commit()
        else:
            return 'change password incorrect'

        return self

    @classmethod
    def get_by_username(cls, username):
        a = SQLManager()
        sql = "SELECT * FROM dbo.account WHERE account_name = \'" + username + "\'"
        a.cursor.execute(sql)
        data = a.cursor.fetchone()
        print('get by username:',data)
        return data

    @classmethod
    def get_by_email(cls, email):
        a = SQLManager()
        sql = "SELECT * FROM dbo.account WHERE email = \'" + email + "\'"
        a.cursor.execute(sql)
        data = a.cursor.fetchone()
        print('get by email:', data)
        return data