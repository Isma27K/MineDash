import sqlite3

class SQLiteHelper:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def fetch_all(self, query, params=()):
        with self.connect() as conn:
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def fetch_one(self, query, params=()):
        with self.connect() as conn:
            cursor = conn.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None

    def execute(self, query, params=()):
        with self.connect() as conn:
            cursor = conn.execute(query, params)
            conn.commit()
            return cursor.lastrowid

    def execute_many(self, query, param_list):
        with self.connect() as conn:
            cursor = conn.executemany(query, param_list)
            conn.commit()
            return cursor.rowcount
