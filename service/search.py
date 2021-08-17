

__all__ = ['Search']

class Search():

    #get waves from selected age and survey type
    @classmethod
    def search_wave(age_type, survey_type):
        wave = []
        '''
        sql search for wave
        wave = str['wave', ...]
        '''
        return wave

    #get problems from selected age, survey, wave 
    @classmethod
    def search_info(age_type, survey_type, wave):
        info = [{'problem_id':'str', 'topic':'str', 'tag':[{'tag_value':'int', 'tag_name':'str'},], 'class':'str', 'exist':[{'type':'int', 'wave':{'young':[{'int':'int'}],'old':[{'int':'int'}]}}]}]
        '''
        sql search for info
        '''
        '''
        sql update user's search info
        '''
        return info

    #get user's last search info: age, survey type
    @classmethod
    def get_search_info(username):
        info = [{'age_type':'int','survey_type':'int','wave':['int','int']}]
        '''
        sql get username search data
        '''
        return info

    #store user's search info
    @classmethod
    def store_search_info(username, info):
        #info = [{'age_type':'int','survey_type':'int','wave':['int','int']}]
        res = "Success"
        '''
        sql save username search data
        '''
        return res

    #delete user's search info: age, survey type
    @classmethod
    def del_search_info(username):
        res = "Success"
        '''
        sql delete username search data
        '''
        return res

    #store user's selected probelm to shop_cart
    @classmethod
    def store_info(username, problem_id):
        res = "Success"
        '''
        sql store to search info
        '''
        '''
        sql store to shopping cart
        '''
        return res

    #get user's shop_cart
    @classmethod
    def get_info(username):
        problem_id = []
        '''
        sql get shopping cart info
        '''
        return problem_id

    #delete user's shop_cart
    @classmethod
    def del_info(username, problem_id):
        res = "Success"
        '''
        sql delete/clear shopping cart info
        '''
        return res