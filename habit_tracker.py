from habits import Habit

class HabitTracker:
    def __init__(self):
        self.habits = []

    def add_habit(self, name, frequency, target_streak):
        habit = Habit(name, frequency, target_streak)
        self.habits.append(habit)
        return habit

    def delete_habit(self, name):
        self.habits = [habit for habit in self.habits if habit.name != name]

    def modify_habit(self, name, new_name=None, new_frequency=None, new_target_streak=None):
        for habit in self.habits:
            if habit.name == name:
                if new_name is not None:
                    habit.name = new_name
                if new_frequency is not None:
                    habit.frequency = new_frequency
                if new_target_streak is not None:
                    habit.target_streak = new_target_streak

    def check_habit(self, name):
        for habit in self.habits:
            if habit.name == name:
                return habit.check()
