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
        survey_op = "SELECT survey_id,age_type,survey_type,wave FROM dbo.survey WHERE release = 1; "
        survey_df=pandas.read_sql(survey_op,self.conn)
        select_survey_df = survey_df[(survey_df['age_type'].isin(combo.age_types) 
                                    & survey_df['survey_type'].isin(combo.survey_types) 
                                    & survey_df['wave'].isin(combo.waves) )]

        create_op = (
        "CREATE TABLE select_survey "
        "( "
        "survey_id INT, "
        "age_type INT, "
        "survey_type INT, "
        "wave INT "
        ") ")
        self.cursor.execute(create_op)
        self.conn.commit()
        self.bulk_insert(select_survey_df,"dbo.select_survey")

        select_survey_prob_op = (
        "SELECT * "
        "FROM dbo.survey_problem "
        "INNER JOIN dbo.select_survey AS ss "
        "ON dbo.survey_problem.survey_id = ss.survey_id "
        "WHERE dbo.survey_problem.release = 1 "
        )

        select_problem_op = (
        "SELECT * "
        "FROM dbo.problem "
        f"INNER JOIN ({select_survey_prob_op}) AS ssp "
        "ON dbo.problem.problem_id = ssp.problem_id "
        )

        class_op = (
        "SELECT * "
        "FROM dbo.class "
        f"INNER JOIN ({select_problem_op}) AS sp "
        "ON dbo.class.class_id = sp.class_id "
        )

        df = pandas.read_sql(class_op)
        self.cursor.excute('DROP TABLE select_survey')
        