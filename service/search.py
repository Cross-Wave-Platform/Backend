

__all__ = ['search_wave', 'search_info', 'store_info', 'get_info', 'del_info']

def search_wave(age_type, survey_type):
    wave = []
    '''
    sql search for wave
    wave = str['wave', ...]
    '''
    return wave

def search_info(age_type, survey_type, wave):
    info = [{'problem_id':'str', 'topic':'str', 'tag':[{'tag_value':'int', 'tag_name':'str'},], 'class':'str', 'exist':[{'type':'int', 'wave':{'young':[{'int':'int'}],'old':[{'int':'int'}]}}]}]
    '''
    sql search for info
    '''
    '''
    sql update user's search info
    '''
    return info

def get_search_info(username):
    info = [{'age_type':'int','survey_type':'int','wave':['int','int']}]
    '''
    sql get username search data
    '''
    return info

def store_info(username, problem_id):
    res = "Success"
    '''
    sql store to search info
    '''
    '''
    sql store to shopping cart
    '''
    return res

def get_info(username):
    problem_id = []
    '''
    sql get shopping cart info
    '''
    return problem_id

def del_info(username, problem_id):
    res = "Success"
    '''
    sql delete/clear shopping cart info
    '''
    return res