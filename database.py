import sqlite3
from habits import Habit
from datetime import datetime

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                frequency INTEGER NOT NULL,
                target_streak INTEGER NOT NULL,
                last_checked DATE,
                streak INTEGER DEFAULT 0,
                points INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def insert_habit(self, name, frequency, target_streak):
        self.cursor.execute('''
            INSERT INTO habits (name, frequency, target_streak) VALUES (?, ?, ?)
        ''', (name, frequency, target_streak))
        self.conn.commit()

    def delete_habit(self, name):
        self.cursor.execute('''
            DELETE FROM habits WHERE name=?
        ''', (name,))
        self.conn.commit()

    def update_habit(self, name, new_name=None, new_frequency=None, new_target_streak=None):
        if new_name is not None:
            self.cursor.execute('''
                UPDATE habits SET name=? WHERE name=?
            ''', (new_name, name))
        if new_frequency is not None:
            self.cursor.execute('''
                UPDATE habits SET frequency=? WHERE name=?
            ''', (new_frequency, name))
        if new_target_streak is not None:
            self.cursor.execute('''
                UPDATE habits SET target_streak=? WHERE name=?
            ''', (new_target_streak, name))
        self.conn.commit()

    def get_all_habits(self):
        self.cursor.execute('''
            SELECT * FROM habits
        ''')
        rows = self.cursor.fetchall()
        habits = []
        for row in rows:
            habit = Habit(row[1], row[2], row[3])
            habit.last_checked = datetime.strptime(row[4], '%Y-%m-%d').date() if row[4] is not None else None
            habit.streak = row[5]
            habit.points = row[6]
            habits.append(habit)
        return habits

    def update_habit_stats(self, habit):
        self.cursor.execute('''
            UPDATE habits SET last_checked=?, streak=?, points=? WHERE name=?
        ''', (habit.last_checked, habit.streak, habit.points, habit.name))
        self.conn.commit()
