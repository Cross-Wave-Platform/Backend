from repo.manager import SQLManager
from flask_login import current_user
from .response import HTTPError

ADMIN_AUTH = 1

def admin_required(func):
    def wrapper(*args,**kwargs):
        manager = SQLManager()
        auth_check = ("SELECT auth FROM dbo.account WHERE account_id = %(account_id)d ")
        manager.cursor.execute(auth_check,{"account_id":current_user.id})
        auth = manager.cursor.fetchone()[0]

        if auth != ADMIN_AUTH:
            return HTTPError('not an admin',403)

        return func(*args,**kwargs)
    return wrapper