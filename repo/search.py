import pandas
from .manager import SQLManager
from .shop_cart import SCManager
from .utils import SURVEY_TYPE, AGE_TYPE


class SearchManager(SQLManager):
    # todo: list age_type,survey_type
    def search_waves(self, age_type, survey_type):
        search_op = ("SELECT wave,age_type,survey_type "
                     "FROM dbo.survey "
                     "WHERE release = 1 ")
        survey_df = pandas.read_sql(search_op, self.conn)
        survey_df = survey_df[survey_df['age_type'].isin(age_type)
                              & survey_df['survey_type'].isin(survey_type)]
        return survey_df

    # use user's last_combo to select surveys
    # return select_prob_df and prob_info_df
    def search_problem(self, account_id):
        combo = SCManager().decode_combo(account_id)
        survey_op = ("SELECT survey_id,age_type,survey_type,wave "
                     "FROM dbo.survey "
                     "WHERE release = 1 ")
        survey_df = pandas.read_sql(survey_op, self.conn)
        select_survey_df = survey_df[(
            survey_df['age_type'].isin(combo.age_types)
            & survey_df['survey_type'].isin(combo.survey_types)
            & survey_df['wave'].isin(combo.waves))]

        create_op = ("CREATE TABLE #select_survey "
                     "( "
                     "survey_id INT, "
                     "age_type INT, "
                     "survey_type INT, "
                     "wave INT "
                     ") ")
        self.cursor.execute(create_op)
        self.conn.commit()
        self.bulk_insert(select_survey_df, "dbo.#select_survey")

        all_select_prob_op = (
            "SELECT select_surv.survey_id,select_surv.age_type,select_surv.survey_type,select_surv.wave, "
            "survey_prob.problem_id "
            "FROM dbo.survey_problem AS survey_prob "
            "INNER JOIN dbo.#select_survey AS select_surv "
            "ON survey_prob.survey_id = select_surv.survey_id "
            "WHERE survey_prob.release = 1 ")

        # drop baby_id
        select_prob_op = (
            "SELECT all_select.survey_id,all_select.age_type,all_select.survey_type,all_select.wave, "
            "all_select.problem_id "
            f"FROM ({all_select_prob_op}) AS all_select "
            "INNER JOIN dbo.problem as prob "
            "ON prob.problem_id = all_select.problem_id "
            "WHERE NOT prob.problem_name = 'baby_id' ")

        select_prob_df = pandas.read_sql(select_prob_op, self.conn)

        select_prob_df['survey_type'].replace(SURVEY_TYPE.inv, inplace=True)
        select_prob_df['age_type'].replace(AGE_TYPE.inv, inplace=True)

        prob_info_op = ("SELECT DISTINCT select_prob.problem_id, "
                        "prob.problem_name,prob.topic,prob.class_id "
                        "FROM dbo.problem AS prob "
                        f"INNER JOIN ({select_prob_op}) AS select_prob "
                        "ON prob.problem_id = select_prob.problem_id ")

        prob_class_op = (
            "SELECT prob_info.problem_id,prob_info.problem_name,prob_info.topic, "
            "cls.class "
            "FROM dbo.class AS cls "
            f"INNER JOIN ({prob_info_op}) AS prob_info "
            "ON cls.class_id = prob_info.class_id ")

        prob_info_df = pandas.read_sql(prob_class_op, self.conn)

        self.cursor.execute('DROP TABLE #select_survey')
        self.conn.commit()

        return select_prob_df, prob_info_df
