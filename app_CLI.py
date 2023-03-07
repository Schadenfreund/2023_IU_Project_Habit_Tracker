from habit_tracker import HabitTracker
from database import Database
from motivational_quotes import MotivationalQuotes
from datetime import date
from colorama import init, Fore, Style

class HabitTrackerApp:
    def __init__(self, db_file, use_demo=False):
        self.use_demo = use_demo
        if self.use_demo:
            db_file = 'demo_habits.db'
            # initialize colorama
            init()
        self.db = Database(db_file)
        self.tracker = HabitTracker()
        self.quotes = MotivationalQuotes()

    def add_habit(self):
        name = input('Enter the name of the habit: ')
        frequency = int(input('Enter the frequency of the habit (1 for daily, 7 for weekly): '))
        target_streak = int(input('Enter the target streak of the habit: '))
        habit = self.tracker.add_habit(name, frequency, target_streak)
        if not self.use_demo:
            self.db.insert_habit(habit.name, habit.frequency, habit.target_streak)

    def delete_habit(self):
        habits = self.db.get_all_habits(use_demo=self.use_demo)
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
            if not self.use_demo:
                self.db.delete_habit(habit_name)
            print(f'The habit "{habit_name}" has been deleted.')
        except (ValueError, IndexError):
            print('Invalid choice.')

    def modify_habit(self):
        habits = self.db.get_all_habits(use_demo=self.use_demo)
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
            new_target_streak = input('Enter the new target streak of the habit (leave blank to not change): ')
            if new_frequency != '':
                new_frequency = int(new_frequency)
            if new_target_streak != '':
                new_target_streak = int(new_target_streak)
            self.tracker.modify_habit(habit_name, new_name, new_frequency, new_target_streak)
            if not self.use_demo:
                self.db.update_habit(habit_name, new_name, new_frequency, new_target_streak)
            print(f'The habit "{habit_name}" has been modified.')
        except (ValueError, IndexError):
            print('Invalid choice.')

    def check_habit(self, use_demo=False):
        habits = self.db.get_all_habits()

        if not habits:
            print('You have no habits.')
            return
        print('Select a habit to check off:')
        for i, habit in enumerate(habits):
            print(f'{i + 1}. {habit.name} ({habit.frequency} days)')
        choice = input('> ')
        try:
            habit = habits[int(choice) - 1]
        except (ValueError, IndexError):
            print('Invalid choice')
            return

        # Check the habit and update stats
        check_date = date.today()
        if habit.check(check_date):
            quote = self.quotes.get_quote()
            print(f'You checked the habit "{habit.name}" on {habit.last_checked}.')
            if habit.streak == 1:
                print(f'Your streak is now {habit.streak}. You have {habit.points} point.')
            else:
                print(f'Your streak is now {habit.streak}. You have {habit.points} points.')
            if habit.streak >= habit.target_streak:
                print(
                    f'Congratulations! You reached your target streak of {habit.target_streak} days for the habit "{habit.name}".')
                print(f'Motivational Quote of the Day: "{quote}"\n')
            self.db.update_habit_stats(habit, use_demo=use_demo)
        else:
            print(f'You have already checked the habit "{habit.name}" today.')

    def list_habits(self):
        habits = self.db.get_all_habits()
        if not habits:
            print('You have no habits.')
        else:
            print(
                f'{Fore.CYAN}{"Habit":<50} {"Frequency":<10} {"Target Streak":<15} {"Streak":<10} {"Points":<10}{Style.RESET_ALL}')
            print('-' * 95)
            for habit in habits:
                habit_name = habit.name
                # change text color for demo mode
                if self.use_demo:
                    habit_name = f'{Fore.RED}{habit.name}{Style.RESET_ALL}'
                print(
                    f'{habit_name:<50} {habit.frequency:<10} {habit.target_streak:<15} {habit.streak:<10} {habit.points:<10}')
    def run(self):
        while True:
            print('Enter an option:')
            print('1. Add a habit')
            print('2. Delete a habit')
            print('3. Modify a habit')
            print('4. Check off a habit')
            print('5. List all habits')
            print('6. Toggle demo mode')
            print('7. Quit')
            choice = input('> ')
            if choice == '1':
                self.add_habit()
            elif choice == '2':
                self.delete_habit()
            elif choice == '3':
                self.modify_habit()
            elif choice == '4':
                self.check_habit()
            elif choice == '5':
                self.list_habits()
            elif choice == '6':
                self.use_demo = not self.use_demo
                if self.use_demo:
                    self.db = Database('demo_habits.db')
                else:
                    self.db = Database('habits.db')
                print(f'Demo mode is {"on" if self.use_demo else "off"}.')
            elif choice == '7':
                break
            else:
                print('Invalid choice')

if __name__ == '__main__':
    app = HabitTrackerApp('habits.db')
    app.run()
