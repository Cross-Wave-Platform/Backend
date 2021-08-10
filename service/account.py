from datetime import datetime, timedelta
from .utils import hash_id
from hmac import compare_digest
import pymssql
from flask_login import UserMixin

import os
import re

__all__ = ['Account']

'''
conn = pymssql.connect(server='140.122.63.2',
                        user='',
                        password='',
                        database='',) 
'''
class Account(UserMixin):
    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.id

    @classmethod
    def signup(cls, username, password, email):
        if re.match(r'^[a-zA-Z0-9_\-]+$', username) is None:
            raise ValueError
        user = cls(username)
        print(user, user.username)
        #user_id = hash_id(user.username, password)# hash password len:24
        user_id = hash_id(username, password)
        #email = email.lower().strip()
        user = cls.get_by_email(email)
        if user is not None:
            return 'email used'
        user = cls.get_by_username(username)
        if user is not None:
            return 'account exists'
        '''
        cursor = conn.cursor()
        sql = 'INSERT dbo.account (user_id, account_name, email, password) OUTPUT INSERT accountID VALUES (\''+ username + '\', \'' + username + '\', \'' + email + '\', \'' + user_id + '\')'
        cursor.execute(sql)
        conn.commit()
        '''
        return user.reload()

    @classmethod
    def login(cls, username, password):
        try:
            user = cls.get_by_username(username)
        except:
            user = cls.get_by_email(username)
        if user is None:
            return 'user not found'
        user_id = hash_id(user.username, password)
        if compare_digest(user.password, user_id):
            return user
        else:
            return 'password incorrect'

    def change_password(self, old_password, new_password):
        user_id = hash_id(self.id, old_password)
        #save new password in db

        return self

    @classmethod
    def get_by_username(cls, username):
        obj = "sql..."
        '''
        sql search by username
        '''
        return obj

    @classmethod
    def get_by_email(cls, email):
        obj = "sql..."
        '''
        sql search by email
        '''
        return obj