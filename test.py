import pandas

problem_list = [
            {"problem_id":"111","survey_id":[1,2]},
            {"problem_id":"222","survey_id":[2,3]}
        ]
res = []
for row in problem_list:
    for id in row['survey_id']:
        tmp = {"problem_id":row['problem_id'],"survey_id":id}
        res.append(tmp)

df = pandas.DataFrame(res)

problem_list = []
df = df.groupby('problem_id')
for key, item in df:
    problem_list.append({"problem_id":key,"survey_id":item['survey_id'].tolist()})

print(problem_list)