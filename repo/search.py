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

    # use user's last_combo to select surveys
    # return select_prob_df and prob_info_df
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

        select_prob_op = (
        "SELECT select_surv.survey_id,select_surv.age_type,select_surv.survey_type,select_surv.wave, "
               "survey_prob.problem_id "
        "FROM dbo.survey_problem AS survey_prob "
        "INNER JOIN dbo.#select_survey AS select_surv "
        "ON survey_prob.survey_id = select_surv.survey_id "
        "WHERE survey_prob.release = 1 "
        )
        select_prob_df = pandas.read_sql(select_prob_op,self.conn)
        
        survey_type_dict = {1:'teacher',2:'parent',3:'friend'}
        select_prob_df['survey_type'].replace(survey_type_dict,inplace=True)
        age_type_dict = {1:'small',2:'big'}
        select_prob_df['age_type'].replace(age_type_dict,inplace=True)

        prob_info_op = (
        "SELECT DISTINCT select_prob.problem_id, "
                "prob.problem_name,prob.topic,prob.class_id "
        "FROM dbo.problem AS prob "
        f"INNER JOIN ({select_prob_op}) AS select_prob "
        "ON prob.problem_id = select_prob.problem_id "
        )

        prob_class_op = (
        "SELECT prob_info.problem_id,prob_info.problem_name,prob_info.topic, "
        "cls.class "
        "FROM dbo.class AS cls "
        f"INNER JOIN ({prob_info_op}) AS prob_info "
        "ON cls.class_id = prob_info.class_id "
        )
        
        prob_info_df = pandas.read_sql(prob_class_op,self.conn)
        
        self.cursor.execute('DROP TABLE #select_survey')
        self.conn.commit()

        return select_prob_df,prob_info_df
        