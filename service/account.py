from datetime import datetime, timedelta
from .utils import hash_id
from hmac import compare_digest
import pymssql
#from engine_config import conn
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
        if not user:
            return 'email used'
        user = cls.get_by_username(username)
        if not user:
            return 'account exists'
        
        user_id = hash_id(username, password)

        # with conn.cursor() as cursor:
        #     sql = "INSERT INTO dbo.account (account_name, email, password) OUTPUT INSERT accountID VALUES ( \'" + username + "\', \'" + email + "\', \'" + user_id + "\')"
        #     cursor.execute(sql)
        #     conn.commit()
        
        return user.reload()

    @classmethod
    def login(cls, username, password):
        try:
            user = cls.get_by_username(username)
        except:
            user = cls.get_by_email(username)
        if user is None:
            return 'user not found'
        user_id = hash_id(user.account_name, password)
        if compare_digest(user.password, user_id):
            return user
        else:
            return 'password incorrect'

    def change_password(self, old_password, new_password):
        user_id = hash_id(self.account_name, old_password)
        if compare_digest(self.password, user_id):
            user_id = hash_id(self.account_name, new_password)
            # with conn.cursor() as cursor:
            #     sql = "UPDATE dbo.account SET password = \'" + user_id + "\' WHERE account_name = \'" + self.account_name + "\'"
            #     cursor.execute(sql)
            #     conn.commit()
        else:
            return 'change password incorrect'

        return self

    @classmethod
    def get_by_username(cls, username):
        # with conn.cursor(as_dict=True) as cursor:
        #     sql = "SELECT * FROM dbo.account WHERE account_name = \'" + username + "\'"
        #     cursor.execute(sql)
        #     data = cursor.fetchone()
        return #data

    @classmethod
    def get_by_email(cls, email):
        # with conn.cursor(as_dict=True) as cursor:
        #     sql = "SELECT * FROM dbo.account WHERE email = \'" + email + "\'"
        #     cursor.execute(sql)
        #     data = cursor.fetchone()
        return #data