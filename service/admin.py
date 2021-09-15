from repo.admin import AdminSQLManager

class NoneLevel(ValueError):
    pass

class AuthError(ValueError):
    pass

class NoneAccount(ValueError):
    pass

__all__ = ['Admin']

class NonedataError(Exception):
    pass
class Admin():
    @classmethod
    def user_management(cls, Identity):
        dict = {
            'All': 'all',
            'admin': '1',
            'member': '2',
            'blacklist': '3'
        }
        if Identity in dict:
            Identity = dict[Identity]

            manager = AdminSQLManager()
            user = manager.user_management(Identity)
        else:
            raise ValueError
        return user

    @classmethod
    def change_auth(cls, user, userlevel):
        dict = {
            'All_superadmin': '1',
            'admin': '1',
            'member': '2',
            'blacklist': '3'
        }
        if cls.check_auth(user) != 0:
            manager = AdminSQLManager()
            if manager.check_account(user) is not None:
                if userlevel in dict:
                    userlevel = dict[userlevel]
                else:
                    raise NoneLevel

                manager.change_auth(user, userlevel)
            else:
                raise NoneAccount
        else:
            raise AuthError

    @classmethod
    def search_by_auth(cls, auth):
        dict = {
            'All_data': 'all',
            'release': '1',
            'unreleased': '0'
        }
        if auth in dict:
            auth = dict[auth]
            manager = AdminSQLManager()
            user = manager.search_by_auth(auth)
        else:
            raise ValueError
        return user

    @classmethod
    def search_by_month(cls, month):
        dict = {
            'Month_all': 'all',
            'Month_small': '1',
            'Month_big': '2'
        }
        if month in dict:
            month = dict[month]
            manager = AdminSQLManager()
            list = manager.search_by_month(month)
        else:
            raise ValueError
        return list

    @classmethod
    def search_by_wave(cls, wave):
        if 'Wave_' in wave:
            wave = wave[5:]
            manager = AdminSQLManager()
            list = manager.search_by_wave(wave)
        else:
            raise ValueError
        return list

    @classmethod
    def search_by_type(cls, type):
        dict = {
            'Allpeople': 'all',
            'Teachers': '1',
            'Parent': '2',
            'Relatives': '3'
        }
        if type in dict:
            type = dict[type]
            manager = AdminSQLManager()
            list = manager.search_by_type(type)
        else:
            return ValueError
        return list

    @classmethod
    def release_survey(cls, DataId, Release):
        manager = AdminSQLManager()
        if manager.is_survey_exists(DataId) is not None:
            manager.release_survey(DataId, Release)
        else:
            raise NonedataError

    @classmethod
    def check_auth(cls, user):
        manager = AdminSQLManager()
        data = manager.check_auth(user)
        return data

