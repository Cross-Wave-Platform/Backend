import pandas
from pandas.core.indexes.api import all_indexes_same


xlsx = pandas.ExcelFile( "../跨波次變項對照表_加入構面.xlsx")

parent = pandas.read_excel( xlsx, sheet_name=0)

teacher = pandas.read_excel( xlsx, sheet_name=1)

friend = pandas.read_excel( xlsx, sheet_name=2)

xlsx.close()

parent = parent[:-4]

teacher = teacher[:-4]

friend = friend[:-4]

all_data = parent.append([ teacher, friend])

columns_to_keep = ['構面', 'min_auth']

# get the unique ones
df = all_data.drop_duplicates(subset=['構面'])

df['min_auth'] = 4

df = df.loc[:, columns_to_keep]

nothing = pandas.DataFrame([['no_group', 4]], columns=['構面', 'min_auth'])

df = pandas.concat( [nothing, df])

df.to_csv( "../all_auth.csv", index=False)

# save the problems tables

columns_to_keep = ['變項名稱', '變項標籤', '構面']

all_data = all_data.drop_duplicates(subset=['變項名稱'])

all_data = all_data.loc[:, columns_to_keep]

print(all_data)

all_data.to_csv( "../all_problems.csv", index=False)




import pymssql

server = "localhost"
user = "SA"
password = "SQLadmin1"

conn = pymssql.connect(server, user, password, "KIT_DB")
cursor = conn.cursor()

BULK_INSERT_ALL_AUTH = r"BULK INSERT dbo.auth FROM '/home/linux/Desktop/MSSQL/all_auth.csv' WITH ( CODEPAGE='RAW', FIRSTROW=2, FORMAT='CSV');"

BULK_INSERT_ALL_PROBLEMS = r"BULK INSERT dbo.problems FROM '/home/linux/Desktop/MSSQL/all_problems.csv' WITH ( CODEPAGE='RAW', FIRSTROW=2, FORMAT='CSV');"

cursor.execute( BULK_INSERT_ALL_AUTH)

conn.commit()

cursor.execute( BULK_INSERT_ALL_PROBLEMS)

conn.commit()

conn.close()
