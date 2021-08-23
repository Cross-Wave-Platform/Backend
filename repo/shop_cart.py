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
    def bind_combo(self,account_id:str,combo:Combo):
        str_age_list = map(str,combo.age_types)
        str_survey_list = map(str,combo.survey_types)
        str_wave_list = map(str,combo.waves)

        c_list=[]
        c_list.append(','.join(str_age_list))
        c_list.append(','.join(str_survey_list))
        c_list.append(','.join(str_wave_list))
        combo='_'.join(c_list)

        bind_op = "UPDATE dbo.account SET last_combo=%(combo)s WHERE account_id=%(account_id)d"
        self.cursor.execute(bind_op,{'combo':combo,'account_id':account_id})
        self.conn.commit()

    def decode_combo(self,account_id:str):
        select_op = "SELECT last_combo FROM dbo.account WHERE account_id=%(account_id)d"
        self.cursor.execute(select_op,{'account_id':account_id})
        combo = self.cursor.fetchone()[0]

        c_list=combo.split('_')
        str_age_list=c_list[0].split(',')
        str_survey_list=c_list[1].split(',')
        str_wave_list=c_list[2].split(',')

        age_types = list(map(int,str_age_list))
        survey_types = list(map(int,str_survey_list))
        waves = list(map(int,str_wave_list))

        return Combo(age_types,survey_types,waves)
        

    def unbind_combo(self,account_id):
        # bind empty combo
        self.bind_combo( account_id, Combo([],[],[]))

    def update_cart(self,account_id:int,cart_df):
        self.clear_cart(account_id)
        cart_df['account_id']=account_id
        cart_df = cart_df[['account_id','survey_id','problem_id']]
        self.bulk_insert(cart_df,"dbo.shop_cart")

    def get_cart(self,account_id):
        get_op = "SELECT survey_id,problem_id FROM dbo.shop_cart WHERE account_id = %(account_id)d"
        return pandas.read_sql(get_op,params={'account_id':account_id})
    
    def clear_cart(self,account_id):
        remove_op = "DELETE FROM dbo.shop_cart WHERE account_id=%(account_id)d"
        self.cursor.execute(remove_op,{'account_id':account_id})
        self.conn.commit()