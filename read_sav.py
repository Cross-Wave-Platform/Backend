import pyreadstat
import pandas

df, meta = pyreadstat.read_sav('../KIT3月齡組第1波3月齡家長_final.sav')

# done! let's see what we got
# print(df.head())
# print(meta.column_names)
# print(meta.column_labels)
# print(meta.column_names_to_labels)
# print(meta.number_rows)
# print(meta.number_columns)
# print(meta.file_label)
# print(meta.file_encoding)
# print(meta.original_variable_types) # this is for the data type reffered by sav files
# there are other metadata pieces extracted. See the documentation for more details.

# these values should be given
answer_value = 1
survey_id = 1

# generating the survey_problem table
survey_problems = pandas.DataFrame()

survey_problems['problems'] = meta.column_names

survey_problems['survey_id'] = survey_id

column_names = ['survey_id','problems']

survey_problems = survey_problems.loc[:,column_names]

# print( survey_problems)
survey_problems.to_csv("../survey_problems.csv", index=False)


# generating answers table
answers = pandas.DataFrame()

all_rows = []

(answer_count, problem_count) = df.shape

# this has the columns ['variable', 'value'] in position
answers = df.T.melt().rename(columns={'variable':'answer_id'})

answers['survey_id'] = survey_id

answers['problem_id'] = meta.column_names*answer_count

column_names = ['answer_id', 'survey_id', 'problem_id', 'value']

answers = answers.loc[:,column_names]

answers['answer_id'] = answers['answer_id'] + answer_value

# print( answers)
answers.to_csv("../answers.csv", index=False)
