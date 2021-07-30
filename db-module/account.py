from datetime import datetime, timedelta
from .utils import hash_id
from hmac import compare_digest
import pymssql

import jwt
import os
import re

__all__ = ['Account', 'jwt_decode']

JWT_EXP = timedelta(days=int(os.environ.get('JWT_EXP', '30')))
JWT_ISS = os.environ.get('JWT_ISS', 'test.test')
JWT_SECRET = os.environ.get('JWT_SECRET', 'SuperSecretString')
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

    def jwt(self, *keys, secret=False, **kwargs):
        if not self:
            return ''
        user = self.reload().to_mongo()
        user['username'] = user.get('_id')
        data = {k: user.get(k) for k in keys}
        data.update(kwargs)
        payload = {
            'iss': JWT_ISS,
            'exp': datetime.now() + JWT_EXP,
            'secret': secret,
            'data': data
        }
        return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def jwt_decode(token):
    try:
        json = jwt.decode(token,
                          JWT_SECRET,
                          issuer=JWT_ISS,
                          algorithms='HS256')
    except jwt.exceptions.PyJWTError:
        return None
    return json