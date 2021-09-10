from .manager import SQLManager


class AccountSQLManager(SQLManager):
    def add_account(self, username: str, hash_in: str, email: str):
        insert_op = 'INSERT INTO dbo.account (account_name, password, email) VALUES (%(username)s, %(email)s, %(password)s)'
        self.cursor.execute(insert_op, {
            'username': username,
            'password': hash_in,
            'email': email
        })
        self.conn.commit()

    def change_password(self, username: str, hash_new: str):
        change_op = 'UPDATE dbo.account SET password=%(new_password)s WHERE account_name=%(username)s'
        self.cursor.execute(change_op, {
            'username': username,
            'new_password': hash_new
        })
        self.conn.commit()

    def change_nickname(self, username: str, nickname: str):
        change_op = 'UPDATE dbo.account SET nickname=%(nickname)s WHERE account_name=%(username)s'
        self.cursor.execute(change_op, {
            'username': username,
            'nickname': nickname
        })
        self.conn.commit()

    def get_by_username(self, username: str):
        search_op = 'SELECT * FROM dbo.account WHERE account_name=%(username)s'
        try:
            self.cursor.execute(search_op, {'username': username})
        except:
            return None
        data = self.cursor.fetchone()
        return data

    def get_by_email(self, email: str):
        search_op = 'SELECT * FROM dbo.account WHERE email=%(email)s'
        try:
            self.cursor.execute(search_op, {'email': email})
        except:
            return None
        data = self.cursor.fetchone()
        return data
