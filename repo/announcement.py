import pandas
from .manager import SQLManager


class AnnouncementManager(SQLManager):
    
    def query_announcement(self, id: int):
        search_op = 'SELECT * FROM dbo.announcement WHERE id=%(id)d'
        try:
            self.cursor.execute(search_op, {'id': id})
        except:
            return None
        data = self.cursor.fetchone()
        index = ["id", "title", "contents", "modifyDate", "pinned"]
        return dict(zip(index, data))

    def list_announcement(self):
        try:
            self.cursor.execute("SELECT id, title, modifyDate, pinned FROM dbo.announcement ORDER BY pinned DESC, modifyDate DESC")
        except:
            return None
        data = self.cursor.fetchall()
        dictList = []
        index = ["id", "title", "modifyDate", "pinned"]
        for dataList in data:
            dataDict = dict(zip(index, dataList))
            dictList.append(dataDict)
        return dictList

    def create_announcement(self, title: str, contents: str, pinned: int):
        insert_op = 'INSERT INTO dbo.announcement (title, contents, modifyDate, pinned) VALUES (%(title)s, %(contents)s, GETDATE(), %(pinned)d)'
        self.cursor.execute(
            insert_op, {
                'title': title,
                'contents': contents,
                'pinned': pinned
            })
        self.conn.commit()

    def update_announcement(self, id: int, title: str, contents: str, pinned: int):
        change_op = 'UPDATE dbo.announcement SET title=%(title)s, contents=%(contents)s, modifyDate=GETDATE(), pinned=%(pinned)d WHERE id = %(id)d'
        self.cursor.execute(change_op, {
            'title': title,
            'contents': contents,
            'pinned': pinned,
            'id': id
        })
        self.conn.commit()

    def delete_announcement(self, id: int):
        delete_op = 'DELETE FROM dbo.announcement WHERE id=%(id)d'
        self.cursor.execute(delete_op, {'id': id})
        self.conn.commit()