import sqlite3
from datetime import datetime, timedelta
from habit_tracker import Habit
from database import Database


def populate_database():
    db = Database("demo_habits.db")

    # Define example daily habits
    daily_habits = [
        Habit("Drink 8 glasses of water", 1, 28, 3, 0),  # Followed for 3 days
        Habit("Exercise for 30 minutes", 1, 28, 7, 0),  # Neglected for 7 days
        Habit("Read for 30 minutes", 1, 28, 0, 0),  # Not attempted yet
        Habit("Meditate for 10 minutes", 1, 28, 14, 0),  # Followed for 14 days
        Habit("Write in journal", 1, 28, 0, 0),  # Not attempted yet
    ]

    # Define example weekly habits
    weekly_habits = [
        Habit("Go to bed before 11pm", 7, 28, 14, 0),  # Followed for 14 days
        Habit("Do a daily task for a big project", 7, 28, 21, 0),  # Followed for 21 days
        Habit("No alcohol", 7, 28, 0, 0),  # Not attempted yet
        Habit("Stretch for 10 minutes", 7, 28, 7, 0),  # Followed for 7 days
        Habit("Practice deep breathing", 7, 28, 0, 0),  # Not attempted yet
        Habit("Do something creative", 7, 28, 14, 0),  # Followed for 14 days
        Habit("YOLO something", 7, 28, 0, 0),  # Not attempted yet
    ]

    # Add habits to database
    for habit in daily_habits + weekly_habits:
        db.insert_habit(habit.name, habit.frequency, habit.target_streak)

    # Check off habits for four weeks
    today = datetime.now().date()
    for i in range(28):
        date = today - timedelta(days=i)
        for habit in db.get_all_habits():
            if habit.frequency == 1 and (habit.last_checked is None or (date - habit.last_checked).days >= 1):
                habit.check(date)
                db.update_habit_stats(habit)
            elif habit.frequency == 7 and (habit.last_checked is None or (date - habit.last_checked).days >= 7):
                habit.check(date)
                db.update_habit_stats(habit)


if __name__ == "__main__":
    populate_database()
