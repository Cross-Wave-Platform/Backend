import sys
sys.path.append('.')

'''
add problems
'''
# from repo.upload import UploadManager,SurveyInfo

# umanager =UploadManager()
# umanager.upload_sav('/home/lil0w1/KIT/Backend/KIT3月齡組第1波3月齡親友_final.sav',SurveyInfo(1,2,3,1))
# umanager.upload_sav('/home/lil0w1/KIT/Backend/KIT3月齡組第1波3月齡親友_final.sav',SurveyInfo(1,2,6,1))

'''
add account and combo
'''
# from repo.shop_cart import Combo, SCManager
# sc_manager = SCManager()
# account_op = "INSERT INTO dbo.account (email,password) VALUES ('1','2')"
# sc_manager.cursor.execute(account_op)
# sc_manager.conn.commit()

# sc_manager.bind_combo(1,Combo([1],[2],[3,6]))

'''
search problem
'''
from repo.search import SearchManager
s_manager = SearchManager()
select_prob_df,prob_info_df=s_manager.search_problem(1)
select_prob_df.to_csv('select_prob.csv')
prob_info_df.to_csv('prob_info.csv')
