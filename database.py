import sqlite3
from habits import Habit
from datetime import datetime


class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                frequency INTEGER NOT NULL,
                last_checked DATE,
                streak INTEGER DEFAULT 0,
                points INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def insert_habit(self, name, frequency):
        self.cursor.execute('''
            INSERT INTO habits (name, frequency) VALUES (?, ?)
        ''', (name, frequency))
        self.conn.commit()

    def delete_habit(self, name):
        self.cursor.execute('''
            DELETE FROM habits WHERE name=?
        ''', (name,))
        self.conn.commit()

    def update_habit(self, name, new_name=None, new_frequency=None):
        if new_name is not None:
            self.cursor.execute('''
                UPDATE habits SET name=? WHERE name=?
            ''', (new_name, name))
        if new_frequency is not None:
            self.cursor.execute('''
                UPDATE habits SET frequency=? WHERE name=?
            ''', (new_frequency, name))
        self.conn.commit()

    def get_all_habits(self):
        self.cursor.execute('''
            SELECT * FROM habits
        ''')
        rows = self.cursor.fetchall()
        habits = []
        for row in rows:
            habit = Habit(row[1], row[2])
            habit.last_checked
            habit.last_checked = datetime.strptime(row[3], '%Y-%m-%d').date() if row[3] is not None else None
            habit.streak = row[4]
            habit.points = row[5]
            habits.append(habit)
        return habits

    def update_habit_stats(self, habit):
        self.cursor.execute('''
            UPDATE habits SET last_checked=?, streak=?, points=? WHERE name=?
        ''', (habit.last_checked, habit.streak, habit.points, habit.name))
        self.conn.commit()