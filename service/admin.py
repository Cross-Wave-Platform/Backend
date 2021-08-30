from repo.manager import SQLManager

__all__ = ['']


def user_management(Identity):
    dict = {
        'All_superadmin': '1',
        'admin': '1',
        'member': '2',
        'blacklist': '3'
    }
    if Identity in dict:
        Identity = dict[Identity]
        a = SQLManager()
        a.conn.cursor(as_dict=True)
        sql = "SELECT account_name, email, auth FROM dbo.account WHERE auth = " + Identity
        a.cursor.execute(sql)
        user = a.cursor.fetchall()
    else:
        raise ValueError
    return user


def change_auth(user, userlevel):
    '''
    sql change auth
    '''
    return 'ok'


def search_by_auth(auth):
    dict = {'All_data': '1 | auth = 0', 'release': '1', 'unreleased': '0'}
    if auth in dict:
        Identity = dict[auth]
        a = SQLManager()
        a.conn.cursor(as_dict=True)
        sql = "SELECT account_name, email, auth FROM dbo.account WHERE auth = " + Identity
        a.cursor.execute(sql)
        user = a.cursor.fetchall()
    else:
        raise ValueError
    return user


def search_by_month(month):
    list = []
    '''
    sql search by month
    '''
    return list


def search_by_wave(wave):
    list = []
    '''
    sql search by wave
    '''
    return list


def search_by_type(type):
    list = []
    '''
    sql search by type
    '''
    return list


def search_by_keyword(keyword):
    list = []
    '''
    sql search by keywords
    '''
    return list


if __name__ == '__main__':
    #current_user.auth = 1
    try:
        a = user_management('member')
        for i in a:
            print(i)
    except ValueError:
        print('ValueError')
    except:
        print('unknown exception')
