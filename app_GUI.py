import tkinter as tk
from habit_tracker import HabitTracker
from database import Database


class HabitTrackerGUI:
    def __init__(self, db_file):
        self.db = Database(db_file)
        self.db.create_table()
        self.tracker = HabitTracker()

        # create main window
        self.root = tk.Tk()
        self.root.title('Habit Tracker')

        # create input fields
        name_label = tk.Label(self.root, text='Name')
        name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1)

        frequency_label = tk.Label(self.root, text='Frequency (1 for daily, 7 for weekly)')
        frequency_label.grid(row=1, column=0)
        self.frequency_entry = tk.Entry(self.root)
        self.frequency_entry.grid(row=1, column=1)

        # create buttons
        add_button = tk.Button(self.root, text='Add', command=self.add_habit)
        add_button.grid(row=2, column=0)

        delete_button = tk.Button(self.root, text='Delete', command=self.delete_habit)
        delete_button.grid(row=2, column=1)

        modify_button = tk.Button(self.root, text='Modify', command=self.modify_habit)
        modify_button.grid(row=2, column=2)

        check_button = tk.Button(self.root, text='Check', command=self.check_habit)
        check_button.grid(row=2, column=3)

        # create listbox for displaying habits
        self.habit_listbox = tk.Listbox(self.root)
        self.habit_listbox.grid(row=3, columnspan=4, pady=10)

        # initialize listbox with current habits
        self.update_listbox()

        # create status bar for displaying messages
        self.status_bar = tk.Label(self.root, text='', bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=4, columnspan=4, sticky=tk.W + tk.E)

        # start main loop
        self.root.mainloop()

    def add_habit(self):
        name = self.name_entry.get()
        frequency = int(self.frequency_entry.get())
        habit = self.tracker.add_habit(name, frequency)
        self.db.insert_habit(habit.name, habit.frequency)
        self.update_listbox()
        self.status_bar.config(text=f'Habit "{habit.name}" added.')

    def delete_habit(self):
        selection = self.habit_listbox.curselection()
        if not selection:
            self.status_bar.config(text='No habit selected.')
            return
        name = self.habit_listbox.get(selection)
        self.tracker.delete_habit(name)
        self.db.delete_habit(name)
        self.update_listbox()
        self.status_bar.config(text=f'Habit "{name}" deleted.')

    def modify_habit(self):
        selection = self.habit_listbox.curselection()
        if not selection:
            self.status_bar.config(text='No habit selected.')
            return
        name = self.habit_listbox.get(selection)
        new_name = self.name_entry.get()
        new_frequency = int(self.frequency_entry.get()) if self.frequency_entry.get() else None
        self.tracker.modify_habit(name, new_name, new_frequency)
        self.db.update_habit(name, new_name, new_frequency)
        self.update_listbox()
        self.status_bar.config(text=f'Habit "{name}" modified.')

    def check_habit(self):
        selection = self.habit_listbox.curselection()
        if not selection:
            self.status_bar.config(text='No habit selected.')
            return
        name = self.habit_listbox.get(selection)
        habit = self.tracker.check_habit(name)
        if habit is not None:
            self.db.update_habit_stats(habit)
            self.update_listbox()
            self.status_bar.config(
                text=f'Habit "{habit.name}" checked on {habit.last_checked}. Streak: {habit.streak}, Points: {habit.points}')
        else:
            self.status_bar.config(text=f'Habit "{name}" does not exist.')

    def update_listbox(self):
        habits = self.db.get_all_habits()
        self.habit_listbox.delete(0, tk.END)
        for habit in habits:
            self.habit_listbox.insert(tk.END,
                                      f'{habit.name} ({habit.frequency} days): {habit.points} points, {habit.streak} day streak')

    def check_habit(self):
        selection = self.habit_listbox.curselection()
        if not selection:
            self.status_bar.config(text='No habit selected.')
            return
        name = self.habit_listbox.get(selection)
        habit = self.tracker.check_habit(name)
        if habit is not None:
            self.db.update_habit_stats(habit)
            self.update_listbox()
            self.status_bar.config(
                text=f'Habit "{habit.name}" checked on {habit.last_checked}. Streak: {habit.streak}, Points: {habit.points}')
        else:
            self.status_bar.config(text=f'Habit "{name}" does not exist.')

    def update_listbox(self):
        habits = self.db.get_all_habits()
        self.habit_listbox.delete(0, tk.END)
        for habit in habits:
            self.habit_listbox.insert(tk.END,
                                      f'{habit.name} ({habit.frequency} days): {habit.points} points, {habit.streak} day streak')

gui = HabitTrackerGUI('habits.db')