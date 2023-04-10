import sqlite3
from habits import Habit
from datetime import datetime

class Database:
    def __init__(self, db_file):
        try:
            self.conn = sqlite3.connect(db_file)
            self.cursor = self.conn.cursor()
            self.create_table()
        except Exception as e:
            print(f"Error connecting to database: {e}")

    def create_table(self):
        try:
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
        except Exception as e:
            print(f"Error creating table: {e}")

    def insert_habit(self, name, frequency, target_streak):
        try:
            self.cursor.execute('''
                INSERT INTO habits (name, frequency, target_streak) VALUES (?, ?, ?)
            ''', (name, frequency, target_streak))
            self.conn.commit()
        except Exception as e:
            print(f"Error inserting habit: {e}")

    def delete_habit(self, name):
        try:
            self.cursor.execute('''
                DELETE FROM habits WHERE name=?
            ''', (name,))
            self.conn.commit()
        except Exception as e:
            print(f"Error deleting habit: {e}")

    def update_habit(self, name, new_name=None, new_frequency=None, new_target_streak=None):
        try:
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
        except Exception as e:
            print(f"Error updating habit: {e}")

    def get_all_habits(self, db_file=None):
        try:
            conn = sqlite3.connect(db_file) if db_file else self.conn
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM habits
            ''')
            rows = cursor.fetchall()
            habits = []
            for row in rows:
                habit = Habit(row[1], row[2], row[3])
                habit.last_checked = datetime.strptime(row[4], '%Y-%m-%d').date() if row[4] is not None else None
                habit.streak = row[5]
                habit.points = row[6]
                habits.append(habit)
            if db_file:
                conn.close()
            return habits
        except Exception as e:
            print(f"Error getting all habits: {e}")

    def update_habit_stats(self, habit, use_demo=False):
        try:
            if use_demo:
                self.cursor.execute('''
                    UPDATE habits SET last_checked=?, streak=?, points=? WHERE name=?
                ''', (habit.last_checked, habit.streak, habit.points, habit.name))
            else:
                self.cursor.execute('''
                    UPDATE habits SET last_checked=?, streak=?, points=? WHERE name=?
                ''', (habit.last_checked, habit.streak, habit.points, habit.name))
            self.conn.commit()
        except Exception as e:
            print(f"Error updating habit stats: {e}")
