from .manager import SQLManager
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas

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
        # this part can use pandas.Dataframe.to_sql() maybe this will help with the speed?
        del_op = "DELETE FROM dbo.shop_cart WHERE account_id=%(account_id)d AND problem_id=%(problem_id)d"
        for r in right_df['problem_id'].tolist():
            self.cursor.execute(del_op,{'account_id':account_id,'problem_id':r})
        
        self.conn.commit()

        # append new collection
        left_df=merge_df[merge_df['_merge']=='left_only'].drop('_merge','columns')
        left_df['account_id']=account_id
        left_df=left_df[['account_id','problem_id']]
        self.bulk_insert(left_df,'dbo.shop_cart')
        
    
    def clear_cart(self,account_id):
        remove_op = "DELETE FROM dbo.shop_cart WHERE account_id=%(account_id)d"
        self.cursor.execute(remove_op,{'account_id':account_id})
        self.conn.commit()
    
    def unbind(self,account_id):
        unbind_op = "UPDATE dbo.account SET last_combo='' WHERE account_id=%(account_id)d"
        self.cursor.execute(unbind_op,{'account_id':account_id})
        self.conn.commit()
    
    def add_problem(self,account_id,problem_id):
        add_op = f'INSERT INTO dbo.shop_cart VALUES ({account_id},{problem_id})'
        self.cursor.execute(add_op)
        self.conn.commit()

