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
    sql = "SELECT * FROM dbo.account WHERE account_id = %(user_id)s"
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


class EmailUsed(ValueError):
    pass


class AccountUsed(ValueError):
    pass


class UserNotFound(ValueError):
    pass


class PasswordIncorrect(ValueError):
    pass


class Account(UserMixin):
    def __init__(self, user_info):
        self.id = user_info['account_id']
        self.account_name = user_info['account_name']
        self.email = user_info['email']
        self.password = user_info['password']

    def get_id(self):
        return self.id

    @classmethod
    def signup(cls, username, password, email):
        if re.match(r'^[a-zA-Z0-9_\-]+$', username) is None:
            raise ValueError
        print('in signup')
        user = cls.get_by_email(email)
        if user is not None:
            raise EmailUsed
        user = cls.get_by_username(username)
        if user is not None:
            raise AccountUsed
        print('ok', user )
        hash_password = hash_id(username, password)

        manager = AccountSQLManager()
        manager.add_account(username, email, hash_password)

    @classmethod
    def login(cls, username, password):
        user = cls.get_by_username(username, as_dict=True) or cls.get_by_email(username, as_dict=True)
        if user is None:
            raise UserNotFound
        account = Account(user)
        user_id = hash_id(account.account_name, password)
        if compare_digest(account.password, user_id):
            return account
        else:
            raise PasswordIncorrect

    def change_password(self, old_password, new_password):
        user_id = hash_id(self.account_name, old_password)
        if compare_digest(self.password, user_id):
            hash_password = hash_id(self.account_name, new_password)
            manager = AccountSQLManager()
            manager.change_password(self.account_name, hash_password)
        else:
            raise PasswordIncorrect
        return self
    
    def change_nickname(self, new_nickname):
        manager = AccountSQLManager()
        manager.change_nickname(self.account_name, new_nickname)
        return self

    def loadinfo(self):
        manager = AccountSQLManager()
        user = manager.loadinfo(self.account_name)
        return user

    @classmethod
    def get_by_username(cls, username, as_dict=False):
        manager = AccountSQLManager(asdict=as_dict)
        data = manager.get_by_username(username)
        return data

    @classmethod
    def get_by_email(cls, email, as_dict=False):
        manager = AccountSQLManager(asdict=as_dict)
        data = manager.get_by_email(email)
        return data
