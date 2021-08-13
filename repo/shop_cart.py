from .manager import SQLManager
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas

class Combo():
    def __init__(self,age_types:list,survey_types:list,waves:list):
        self.age_types=age_types
        self.survey_types=survey_types
        self.waves=waves

class SCManager(SQLManager):
    def update(self,account_id:int,collection:list):
        check_op = ("SELECT problem_id "
                    "FROM dbo.shop_cart "
                    "WHERE account_id = %(account_id)s")

        old_collection = pandas.read_sql(check_op,self.conn,
                                         params={'account_id':account_id}) 

        given_collection = pandas.DataFrame(collection,columns=['problem_id'])
        merge_df=pandas.merge(given_collection,old_collection,'outer','problem_id',indicator=True)
        right_df=merge_df[merge_df['_merge']=='right_only']

        # remove unncessary collection
        if not right_df.empty:
            r_list=right_df['problem_id'].tolist()
            del_op = f"DELETE FROM dbo.shop_cart WHERE account_id=%d AND problem_id IN ({', '.join('%s' for _ in r_list)})"
            self.cursor.execute(del_op,(account_id,*r_list))

        self.conn.commit()

        # append new collection
        left_df=merge_df[merge_df['_merge']=='left_only'].drop('_merge','columns')
        left_df['account_id']=account_id
        left_df=left_df[['account_id','problem_id']]
        self.bulk_insert(left_df,'dbo.shop_cart')

    def bind_combo(self,account_id:str,combo:Combo):
        c_list=[]
        c_list.append(','.join(combo.age_types))
        c_list.append(','.join(combo.survey_types))
        c_list.append(','.join(combo.waves))
        combo='_'.join(c_list)

        bind_op = "UPDATE dbo.account SET last_combo=%(combo)s WHERE account_id=%(account_id)d"
        self.cursor.execute(bind_op,{'combo':combo,'account_id':account_id})
        self.conn.commit()

    def decode_combo(self,account_id:str):
        select_op = "SELECT last_combo FROM dbo.account WHERE account_id=%(account_id)d"
        self.cursor.execute(select_op,{'account_id':account_id})
        combo = self.cursor.fetchone()[0]

        c_list=combo.split('_')
        age_types=c_list[0].split(',')
        survey_types=c_list[1].split(',')
        waves=c_list[2].split(',')

        return Combo(age_types,survey_types,waves)
        

    def unbind_combo(self,account_id):
        unbind_op = "UPDATE dbo.account SET last_combo='' WHERE account_id=%(account_id)d"
        self.cursor.execute(unbind_op,{'account_id':account_id})
        self.conn.commit()
    
    def clear_cart(self,account_id):
        remove_op = "DELETE FROM dbo.shop_cart WHERE account_id=%(account_id)d"
        self.cursor.execute(remove_op,{'account_id':account_id})
        self.conn.commit()
    