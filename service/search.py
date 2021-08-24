from repo.search import SearchManager
from repo.shop_cart import Combo,SCManager
import pandas

__all__ = ['Search']

class Search():

    #get waves from selected age and survey type
    @classmethod
    def search_wave(cls, age_type, survey_type):
        # wave = ['int','int']
        # print(age_type)
        # print(survey_type)
        manager = SearchManager()
        df = manager.search_waves(age_type,survey_type)
        wave = df['wave'].tolist()
        return wave

    #get problems from selected age, survey, wave 
    @classmethod
    def search_info(cls, id):
        # info = [{'problem_id':'str', 'topic':'str', 'tag':[{'tag_value':'int', 'tag_name':'str'},], 'class':'str', 'exist':[{'type':'int', 'wave':{'young':[{'int':'int'}],'old':[{'int':'int'}]}}]}]
        '''
        sql search for info
        '''
        manager = SearchManager()
        '''
        sql get user's search problems
        '''
        select_prob_df,prob_info_df = manager.search_problem(id)
        '''
        df to dictionary
        '''
        res = {}

        df = prob_info_df
        df_list = df.values.tolist()


        for row in df_list:
            question = {"problem_id":row[1], \
                        "topic":row[2], \
                        "class":row[3], \
                        "survey_id":set(), \
                        "exist":{}
                        }
            res[row[0]] = question
        
        df = select_prob_df
        df_list = df.values.tolist()
        

        for row in df_list:
            id = row[4]
            if row[2] not in res[id]['exist']:
                res[id]['exist'][row[2]] = {"young":[], \
                                                "old":[]}
            if row[1] == "big":
                res[id]['exist'][row[2]]['old'].append(row[3])
            else:
                res[id]['exist'][row[2]]['young'].append(row[3])

            res[id]['survey_id'].add(row[0])
        
        for k, v  in res.items():
            # print(k ,":" , v)
            v['survey_id'] = list(v['survey_id'])

        return res

    #get user's last search info: age, survey type
    @classmethod
    def get_search_info(cls, id):
        '''
        sql get username search data
        '''
        combo = SCManager().decode_combo(id)
        info = {'age_type':combo.age_types,'survey_type':combo.survey_types,'wave':combo.waves}
        return info

    #store user's search info
    @classmethod
    def store_search_info(cls, id, info):
        #info = {'age_type':[],'survey_type':[],'wave':[]}
        '''
        sql save username search data
        '''
        combo = Combo(info['age_type'],info['survey_type'],info['wave'])
        SCManager().bind_combo(id,combo)
        
        res = "Success"
        return res

    #delete user's search info: age, survey type
    @classmethod
    def del_search_info(cls, id):
        '''
        sql delete username search data
        '''
        SCManager().unbind_combo(id)
        res = "Success"
        return res

    #store user's selected probelm to shop_cart
    @classmethod
    def store_info(cls, id, problem_list):
        # problem_list = [
        #     {"problem_id":"111","survey_id":[1,2]},
        #     {"problem_id":"222","survey_id":[2,3]}
        # ]
        res = []
        for row in problem_list:
            for tid in row['survey_id']:
                tmp = {"problem_id":row['problem_id'],"survey_id":tid}
                res.append(tmp)
        res_df = pandas.DataFrame(res)
        '''
        sql store to shopping cart
        '''
        SCManager().update_cart(id,res_df)

        res = "Success"
        return res

    #get user's shop_cart
    @classmethod
    def get_info(cls, id):
        # problem_list = [
        #     {"problem_id":"111","survey_id":[1,2]},
        #     {"problem_id":"222","survey_id":[2,3]}
        # ]
        '''
        sql get shopping cart info
        '''
        df=SCManager().get_cart(id)

        problem_list = []
        df = df.groupby('problem_id')
        for key, item in df:
            problem_list.append({"problem_id":key,"survey_id":item['survey_id'].tolist()})

        return problem_list

    #delete user's shop_cart
    @classmethod
    def del_info(cls, id):
        '''
        sql delete/clear shopping cart info
        '''
        SCManager().clear_cart(id)
        res = "Success"
        
        return res