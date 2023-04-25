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
        return data

    def list_announcement(self):
        try:
            self.cursor.execute("SELECT id, title FROM dbo.announcement ORDER BY id DESC")
        except:
            return None
        data = self.cursor.fetchall()
        return data

    def create_announcement(self, title: str, contents: str):
        insert_op = 'INSERT INTO dbo.announcement (title, contents) VALUES (%(title)s, %(contents)s)'
        self.cursor.execute(
            insert_op, {
                'title': title,
                'contents': contents
            })
        self.conn.commit()

    def update_announcement(self, id: int, title: str, contents: str):
        change_op = 'UPDATE dbo.announcement SET title=%(title)s, contents=%(contents)s WHERE id = %(id)d'
        self.cursor.execute(change_op, {
            'title': title,
            'contents': contents,
            'id': id
        })
        self.conn.commit()

    def delete_announcement(self, id: int):
        delete_op = 'DELETE FROM dbo.announcement WHERE id=%(id)d'
        self.cursor.execute(delete_op, {'id': id})