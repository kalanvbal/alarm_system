import sqlite3
from datetime import datetime

class Model:
    def __init__(self, action=None):
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.action = action

    @staticmethod
    def create_table():
        with sqlite3.connect('alarm_system.db') as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    action TEXT
                )
            ''')
        conn.commit()
        conn.close()

    def save_to_db(self):
        with sqlite3.connect('alarm_system.db') as conn:
            conn.execute('''
                INSERT INTO actions (date, action) VALUES (?, ?)
            ''', (self.date, self.action))

    @staticmethod
    def fetch_actions():
        with sqlite3.connect('alarm_system.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT date, action FROM actions')
            return cursor.fetchall()

    def afficher(self):
        if self.action:
            return f"{self.date}, {self.action} "
