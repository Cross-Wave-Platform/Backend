import flask
from .utils import hash_id
from hmac import compare_digest
import pymssql
import hashlib

import re

__all__ = ['Account']

class Account():
    def __init__(self, username):
        self.username = username

    @classmethod
    def signup(cls, username, password, email):
        if re.match(r'^[a-zA-Z0-9_\-]+$', username) is None:
            raise ValueError
        user = cls(username)
        user_id = hash_id(user.username, password)# hash password len:24
        #email = email.lower().strip()
        '''
        sql save
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
        if compare_digest(user.username, user_id):
            return user
        else:
            return 'password incorrect'

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
