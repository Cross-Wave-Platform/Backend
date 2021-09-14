'''
add problems
'''
from repo.manager import SQLManager
from service.utils import hash_id
'''
add account and combo
'''

sc_manager = SQLManager()
# admin account
password = hash_id('admin', "123")
account_op = "INSERT INTO dbo.account (account_name,nickname,email,password,auth) VALUES ('admin','admin','123',%(password)s,0)"
sc_manager.cursor.execute(account_op, {"password": password})
# normal account
password = hash_id('normal', "456")
account_op = "INSERT INTO dbo.account (account_name,nickname,email,password) VALUES ('normal','normal','456',%(password)s)"
sc_manager.cursor.execute(account_op, {"password": password})
sc_manager.conn.commit()
