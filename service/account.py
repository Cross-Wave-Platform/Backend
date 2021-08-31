from .utils import hash_id
from hmac import compare_digest
from repo.account import AccountSQLManager
from repo.manager import SQLManager
from flask_login import UserMixin, LoginManager
import re

__all__ = ['Account']

login_manager = LoginManager()


def get_user(user_id):
    manager = SQLManager()
    sql = "SELECT * FROM dbo.account WHERE account_name = %(user_id)s"
    manager.cursor.execute(sql, {"user_id": user_id})
    data = manager.cursor.fetchone()
    return data


@login_manager.user_loader
def user_loader(user_id):
    user_info = get_user(user_id)
    if user_info is not None:
        current_user = Account(user_info)
        return current_user
    return None


class Account(UserMixin):
    def __init__(self, user_info):
        self.id = user_info[0]
        self.account_name = user_info[1]
        self.email = user_info[2]
        self.password = user_info[3]

    def get_id(self):
        return self.id

    @classmethod
    def signup(cls, username, password, email):
        if re.match(r'^[a-zA-Z0-9_\-]+$', username) is None:
            raise ValueError

        user = cls.get_by_email(email)
        if user is not None:
            return 'email used'
        user = cls.get_by_username(username)
        if user is not None:
            return 'account exists'

        hash_password = hash_id(username, password)

        manager = AccountSQLManager()
        manager.add_account(username, email, hash_password)
        return 'ok'

    @classmethod
    def login(cls, username, password):
        try:
            user = cls.get_by_username(username)
        except:
            user = cls.get_by_email(username)
        if user is None:
            return 'user not found'
        account = Account(user)
        user_id = hash_id(account.account_name, password)
        if compare_digest(account.password, user_id):
            return account
        else:
            return 'password incorrect'

    def change_password(self, old_password, new_password):
        user_id = hash_id(self.account_name, old_password)
        if compare_digest(self.password, user_id):
            hash_password = hash_id(self.account_name, new_password)
            a = AccountSQLManager()
            a.change_password(self.account_name, hash_password)
        else:
            return 'change password incorrect'
        return self

    @classmethod
    def get_by_username(cls, username):
        manager = AccountSQLManager()
        data = manager.get_by_username(username)
        return data

    @classmethod
    def get_by_email(cls, email):
        manager = AccountSQLManager()
        data = manager.get_by_email(email)
        return data
