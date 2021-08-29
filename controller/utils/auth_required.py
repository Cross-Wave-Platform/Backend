from enum import IntEnum
from flask import current_app
from flask_login import current_user
from functools import wraps
from repo.manager import SQLManager
from .response import HTTPError


class AuthLevel(IntEnum):
    ADMIN = 1
    REGULAR = 2
    BAN = 3


def auth_required(min_auth=AuthLevel.REGULAR):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_app.config.get('AUTH_DISABLED'):
                return func(*args, **kwargs)
            manager = SQLManager()
            auth_check = (
                "SELECT auth FROM dbo.account WHERE account_id = %(account_id)d "
            )
            manager.cursor.execute(auth_check, {"account_id": current_user.id})
            auth = manager.cursor.fetchone()[0]

            if auth > min_auth:
                return HTTPError('auth is not satified', 403)

            return func(*args, **kwargs)

        return wrapper

    return decorator
