import pandas
from .manager import SQLManager
from .shop_cart import SCManager

class SearchManager(SQLManager):
    def search_waves(self, age_type, survey_type):
        search_op = ("SELECT wave "
                     "FROM dbo.survey "
                     "WHERE age_type = %(age_type)s "
                     "AND survey_type = %(survey_type)s "
                     "AND release = 1")
        params = {'age_type': age_type, 'survey_type': survey_type}

        return pandas.read_sql(search_op,self.conn,params=params)

    def search_problem(self,account_id):
        combo = SCManager().decode_combo(account_id)
        survey_op = (
        "SELECT survey_id,age_type,survey_type,wave "
        "FROM dbo.survey "
        "WHERE release = 1 ")
        survey_df=pandas.read_sql(survey_op,self.conn)
        select_survey_df = survey_df[(survey_df['age_type'].isin(combo.age_types) 
                                    & survey_df['survey_type'].isin(combo.survey_types) 
                                    & survey_df['wave'].isin(combo.waves) )]

        create_op = (
        "CREATE TABLE #select_survey "
        "( "
        "survey_id INT, "
        "age_type INT, "
        "survey_type INT, "
        "wave INT "
        ") ")
        self.cursor.execute(create_op)
        self.conn.commit()
        self.bulk_insert(select_survey_df,"dbo.#select_survey")

        select_survey_prob_op = (
        "SELECT ss.survey_id,ss.age_type,ss.survey_type,ss.wave, "
               "survey_prob.problem_id "
        "FROM dbo.survey_problem AS survey_prob "
        "INNER JOIN dbo.#select_survey AS ss "
        "ON survey_prob.survey_id = ss.survey_id "
        "WHERE survey_prob.release = 1 "
        )

        select_prob_op = (
        "SELECT ssp.survey_id,ssp.age_type,ssp.survey_type,ssp.wave,ssp.problem_id, "
               "prob.problem_name,prob.topic,prob.class_id "
        "FROM dbo.problem AS prob "
        f"INNER JOIN ({select_survey_prob_op}) AS ssp "
        "ON prob.problem_id = ssp.problem_id "
        )

        prob_class_op = (
        "SELECT sp.survey_id,sp.age_type,sp.survey_type,sp.wave,sp.problem_id, "
        "sp.problem_name,sp.topic, "
        "cls.class "
        "FROM dbo.class AS cls "
        f"INNER JOIN ({select_prob_op}) AS sp "
        "ON cls.class_id = sp.class_id "
        )
        
        select_prob_df = pandas.read_sql(prob_class_op,self.conn)
        self.cursor.execute('DROP TABLE #select_survey')
        self.conn.commit()
        
        survey_type_dict = {1:'teacher',2:'parent',3:'friend'}
        select_prob_df['survey_type'].replace(survey_type_dict,inplace=True)
        
        age_type_dict = {1:'big',2:'small'}
        select_prob_df['age_type'].replace(age_type_dict,inplace=True)
    
        select_prob_df.to_csv('sample.csv')

        return select_prob_df
        