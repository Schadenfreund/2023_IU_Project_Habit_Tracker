from habits import Habit

class HabitTracker:
    def __init__(self):
        self.habits = []

    def add_habit(self, name, frequency):
        habit = Habit(name, frequency)
        self.habits.append(habit)
        return habit

    def delete_habit(self, name):
        for habit in self.habits:
            if habit.name == name:
                self.habits.remove(habit)

    def modify_habit(self, name, new_name=None, new_frequency=None):
        for habit in self.habits:
            if habit.name == name:
                if new_name is not None:
                    habit.name = new_name
                if new_frequency is not None:
                    habit.frequency = new_frequency

    def check_habit(self, name):
        for habit in self.habits:
            if habit.name == name:
                return habit.check()