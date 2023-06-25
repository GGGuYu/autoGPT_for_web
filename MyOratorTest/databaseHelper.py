import sqlite3

class DatabaseHelper:
    def __init__(self):
        self.conn = sqlite3.connect('memo.db')
        self.create_table()

    def create_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS Memo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memo TEXT
            )
        '''
        self.conn.execute(sql)
        self.conn.commit()

    def add_memo(self, memo):
        sql = "INSERT INTO Memo (memo) VALUES (?)"
        self.conn.execute(sql, [memo])
        self.conn.commit()

    def get_memos(self):
        cursor = self.conn.execute("SELECT * FROM Memo")
        result = []
        for row in cursor:
            result.append(row[1])
        return result