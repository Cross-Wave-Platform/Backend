import pandas

xlsx = pandas.ExcelFile( "跨波次變項對照表_加入構面.xlsx")

parent = pandas.read_excel( xlsx, sheet_name=0)

teacher = pandas.read_excel( xlsx, sheet_name=1)

friend = pandas.read_excel( xlsx, sheet_name=2)

parent = parent[:-4]

teacher = teacher[:-4]

friend = friend[:-4]

print(parent)
print(teacher)
print(friend)

df = parent.append([ teacher, friend])

columns_to_keep = ['構面', 'min_auth']

# get the unique ones
df = df.drop_duplicates(subset=['構面'])

df['min_auth'] = 4

df = df.reset_index(drop=True)

# print(df.drop_duplicates(subset=columns_to_keep))

df.loc[:, columns_to_keep].to_csv( "test.csv")

xlsx.close()
