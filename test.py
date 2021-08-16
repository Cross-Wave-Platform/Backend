import pymssql

conn = pymssql.connect(host='127.0.0.1', user='test', password='zxcppor1227', database='KIT_DB', port=1433)  
print('ok')
cur = conn.cursor(as_dict=True)

#sql = "INSERT INTO dbo.account( account_name, email, password, auth) VALUES( 'testuser', 'test@gmail.com', 'password', 4 )"
#cur.execute(sql)
#conn.commit()
username = 'testuser'

sql = "SELECT * FROM dbo.account WHERE account_name = \'" + username + "\'"
cur.execute(sql)
data = cur.fetchone()


print(data)
if not data:
    print('data is none')

cur.close()
conn.close()