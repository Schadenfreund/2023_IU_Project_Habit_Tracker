import random
import datetime
from habits import Habit
from database import Database

# Initialize database
db = Database('../demo_habits.db')

# Habits to insert
habits_to_insert = [
    ('Drink 8 glasses of water', 7, 28),
    ('Exercise for 60 minutes', 4, 16),
    ('Do Cardio', 7, 28),
    ('Read for 30 minutes', 7, 28),
    ('Write 500 words', 3, 12),
    ('Practice python', 2, 8),
    ('Floss teeth', 7, 28),
    ('Think of something nice', 7, 28),
    ('Play guitar', 7, 28),
    ('Get 8 hours of sleep', 7, 28)
]

# Insert habits
for habit_info in habits_to_insert:
    name, frequency, target_streak = habit_info
    db.insert_habit(name, frequency, target_streak)

# Generate data for 4 weeks
start_date = datetime.date.today() - datetime.timedelta(days=28)
current_date = start_date
end_date = datetime.date.today()
while current_date <= end_date:
    for habit in db.get_all_habits():
        if habit.frequency == 7 or current_date.weekday() == habit.frequency:
            if habit.last_checked is None or habit.last_checked < current_date:
                if random.random() < 0.8:  # 80% chance of success
                    habit.streak += 1
                    habit.points += 1
                else:
                    habit.streak = 0
                habit.last_checked = current_date
                db.update_habit_stats(habit, use_demo=True)
    current_date += datetime.timedelta(days=1)

print("Demo database generated successfully.")