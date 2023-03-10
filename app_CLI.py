from habit_tracker import HabitTracker
from database import Database
from motivational_quotes import MotivationalQuotes


class HabitTrackerApp:
    def __init__(self, db_file):
        self.db = Database(db_file)
        self.db.create_table()
        self.tracker = HabitTracker()
        self.quotes = MotivationalQuotes()

    def add_habit(self):
        name = input('Enter the name of the habit: ')
        frequency = int(input('Enter the frequency of the habit (1 for daily, 7 for weekly): '))
        habit = self.tracker.add_habit(name, frequency)
        self.db.insert_habit(habit.name, habit.frequency)

    def delete_habit(self):
        habits = self.db.get_all_habits()
        if not habits:
            print('You have no habits to delete.')
            return
        print('Select a habit to delete:')
        for i, habit in enumerate(habits):
            print(f'{i + 1}. {habit.name} ({habit.frequency} days): {habit.points} points, {habit.streak} day streak')
        choice = input('> ')
        try:
            habit_index = int(choice) - 1
            habit_name = habits[habit_index].name
            self.tracker.delete_habit(habit_name)
            self.db.delete_habit(habit_name)
            print(f'The habit "{habit_name}" has been deleted.')
        except (ValueError, IndexError):
            print('Invalid choice.')

    def modify_habit(self):
        habits = self.db.get_all_habits()
        if not habits:
            print('You have no habits to modify.')
            return
        print('Select a habit to modify:')
        for i, habit in enumerate(habits):
            print(f'{i + 1}. {habit.name} ({habit.frequency} days): {habit.points} points, {habit.streak} day streak')
        choice = input('> ')
        try:
            habit_index = int(choice) - 1
            habit_name = habits[habit_index].name
            new_name = input(f'Enter the new name of the habit "{habit_name}" (leave blank to not change): ')
            new_frequency = input('Enter the new frequency of the habit (leave blank to not change): ')
            if new_frequency != '':
                new_frequency = int(new_frequency)
            self.tracker.modify_habit(habit_name, new_name, new_frequency)
            self.db.update_habit(habit_name, new_name, new_frequency)
            print(f'The habit "{habit_name}" has been modified.')
        except (ValueError, IndexError):
            print('Invalid choice.')

    def check_habit(self):
        habits = self.db.get_all_habits()
        if not habits:
            print('You have no habits.')
            return
        print('Select a habit to check off:')
        for i, habit in enumerate(habits):
            print(f'{i+1}. {habit.name} ({habit.frequency} days)')
        choice = input('> ')
        try:
            habit = habits[int(choice)-1]
        except (ValueError, IndexError):
            print('Invalid choice')
            return
        self.tracker.check_habit(habit.name)
        self.db.update_habit_stats(habit)
        print(f'You checked the habit "{habit.name}" on {habit.last_checked}. Your streak is now {habit.streak}. You have {habit.points} points.')
        self.show_quote()

    def list_habits(self):
        habits = self.db.get_all_habits()
        if not habits:
            print('You have no habits.')
        else:
            print(f'{"Habit":<50} {"Frequency":<10} {"Streak":<10} {"Points":<10}')
            print('-' * 90)
            for habit in habits:
                print(f'{habit.name:<50} {habit.frequency:<10} {habit.streak:<10} {habit.points:<10}')

    def show_quote(self):
        quote = self.quotes.get_quote()
        print(f'Motivational Quote of the Day: "{quote}"\n')


if __name__ == '__main__':
    app = HabitTrackerApp('habits.db')
    while True:
        print('Enter an option:')
        print('1. Add a habit')
        print('2. Delete a habit')
        print('3. Modify a habit')
        print('4. Check off a habit')
        print('5. List all habits')
        print('6. Quit')
        choice = input('> ')
        if choice == '1':
            app.add_habit()
        elif choice == '2':
            app.delete_habit()
        elif choice == '3':
            app.modify_habit()
        elif choice == '4':
            app.check_habit()
        elif choice == '5':
            app.list_habits()
        elif choice == '6':
            break
        else:
            print('Invalid choice')