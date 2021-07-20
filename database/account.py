import flask
from .utils import hash_id
from hmac import compare_digest
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
        user_id = hash_id(user.username, password)
        #email = email.lower().strip()
        #sql save
        return user.reload()

    @classmethod
    def login(cls, username, password):
        try:
            user = cls.get_by_username(username)
        except:
            user = cls.get_by_email(username)
        user_id = hash_id(user.username, password)
        if compare_digest(user.user_id, user_id) or compare_digest(
                user.user_id2, user_id):
            return user
        raise
