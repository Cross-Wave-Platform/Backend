import pandas
from .manager import SQLManager


class PictureManager(SQLManager):

    def input_picture(self, id:int , picture: bytes):
        insert_op = 'INSERT INTO dbo.picture (id , picture) VALUES (%(id)d, %(picture)s)'
        self.cursor.execute(
            insert_op, {
                'id': id,
                'picture': picture
            })
        self.conn.commit()

    def list_picture(self):
        try:
            self.cursor.execute("SELECT id, picture FROM dbo.picture ORDER BY id DESC")
        except:
            return None
        data = self.cursor.fetchall()
        dictList = []
        index = ["id", "picture"]
        for dataList in data:
            dataDict = dict(zip(index, dataList))
            dictList.append(dataDict)
        return dictList

    def update_picture(self, id: int, picture: bytes):
        change_op = 'UPDATE dbo.picture SET picture=%(picture)s WHERE id = %(id)d'
        self.cursor.execute(change_op, {
            'picture': picture,
            'id': id
        })
        self.conn.commit()

    def delete_picture(self, id: int):
        delete_op = 'DELETE FROM dbo.picture WHERE id=%(id)d'
        self.cursor.execute(delete_op, {'id': id})
        self.conn.commit()