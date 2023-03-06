from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QSpinBox,
    QPushButton, QTextEdit, QMessageBox, QInputDialog
)
from habit_tracker import HabitTracker
from database import Database
from motivational_quotes import MotivationalQuotes
from PyQt5 import QtCore


class HabitTrackerWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Habit Tracker")

        layout = QGridLayout()

        # Add widgets to layout
        habit_name_label = QLabel("Name of habit:")
        layout.addWidget(habit_name_label, 0, 0)

        self.habit_name_edit = QLineEdit()
        layout.addWidget(self.habit_name_edit, 0, 1)

        frequency_label = QLabel("Frequency (1 for daily, 7 for weekly):")
        layout.addWidget(frequency_label, 1, 0)

        self.frequency_spin = QSpinBox()
        self.frequency_spin.setRange(1, 7)
        self.frequency_spin.setValue(1)
        layout.addWidget(self.frequency_spin, 1, 1)

        add_habit_button = QPushButton("Add Habit")
        add_habit_button.clicked.connect(self.add_habit)
        layout.addWidget(add_habit_button, 2, 1)

        self.habit_list = QTextEdit()
        layout.addWidget(self.habit_list, 3, 0, 1, 2)

        delete_habit_button = QPushButton("Delete Habit")
        delete_habit_button.clicked.connect(self.delete_habit)
        layout.addWidget(delete_habit_button, 4, 0)

        modify_habit_button = QPushButton("Modify Habit")
        modify_habit_button.clicked.connect(self.modify_habit)
        layout.addWidget(modify_habit_button, 4, 0)

        check_habit_button = QPushButton("Check Habit")
        check_habit_button.clicked.connect(self.check_habit)
        layout.addWidget(check_habit_button, 4, 1)

        list_habits_button = QPushButton("Update List")
        list_habits_button.clicked.connect(self.list_habits)
        layout.addWidget(list_habits_button, 5, 0)

        quit_button = QPushButton("Quit")
        quit_button.clicked.connect(self.close)
        layout.addWidget(quit_button, 5, 1)

        self.quote_label = QLabel()
        self.quote_label.setWordWrap(True)
        layout.addWidget(self.quote_label, 6, 0, 1, 2)

        self.setLayout(layout)

    def add_habit(self):
        name = self.habit_name_edit.text()
        frequency = self.frequency_spin.value()
        habit = self.tracker.add_habit(name, frequency)
        self.db.insert_habit(habit.name, habit.frequency)
        self.habit_name_edit.setText("")
        self.frequency_spin.setValue(1)
        self.habit_list.setText(self.get_habit_list())

    def delete_habit(self):
        habits = self.db.get_all_habits()
        if not habits:
            QMessageBox.information(self, "No Habits", "You have no habits to delete.")
            return
        habit_names = [habit.name for habit in habits]
        choice, ok = QInputDialog.getItem(self, "Delete Habit", "Select a habit to delete:", habit_names, 0, False)
        if ok:
            habit_name = choice
            self.tracker.delete_habit(habit_name)
            self.db.delete_habit(habit_name)
            QMessageBox.information(self, "Habit Deleted", f"The habit '{habit_name}' has been deleted.")
            self.habit_list.setText(self.get_habit_list())

    def modify_habit(self):
        habits = self.db.get_all_habits()
        if not habits:
            QMessageBox.information(self, "No Habits", "You have no habits to modify.")
            return
        habit_names = [habit.name for habit in habits]
        choice, ok = QInputDialog.getItem(self, "Modify Habit", "Select a habit to modify:", habit_names, 0, False)
        if ok:
            habit_name = choice
            new_name, ok = QInputDialog.getText(self, "Modify Habit",
                                                f"Enter the new name of the habit '{habit_name}' (leave blank to not change):",
                                                QLineEdit.Normal, habit_name)
            if ok:
                new_name = new_name.strip()
                if new_name == "":
                    new_name = habit_name
                new_frequency, ok = QInputDialog.getInt(self, "Modify Habit",
                                                        "Enter the new frequency of the habit (leave blank to not change):",
                                                        value=habits[habit_names.index(habit_name)].frequency, min=1,
                                                        max=7)
                if ok:
                    self.tracker.modify_habit(habit_name, new_name, new_frequency)
                    self.db.update_habit(habit_name, new_name, new_frequency)
                    QMessageBox.information(self, "Habit Modified", f"The habit '{habit_name}' has been modified.")
                    self.habit_list.setText(self.get_habit_list())

    def check_habit(self):
        habits = self.db.get_all_habits()
        if not habits:
            QMessageBox.information(self, "No Habits", "You have no habits to check off.")
            return
        habit_names = [habit.name for habit in habits]
        choice, ok = QInputDialog.getItem(self, "Check Habit", "Select a habit to check off:", habit_names, 0, False)
        if ok:
            habit = habits[habit_names.index(choice)]
            self.tracker.check_habit(habit.name)
            self.db.update_habit_stats(habit)
            QMessageBox.information(self, "Habit Checked", f"You checked the habit '{habit.name}' on {habit.last_checked}. Your streak is now {habit.streak}. You have {habit.points} points.")
            self.habit_list.setText(self.get_habit_list())
            self.show_quote()

    def list_habits(self):
        habits = self.db.get_all_habits()
        if not habits:
            self.habit_list.setText("You have no habits.")
        else:
            habit_list = "<table>"
            habit_list += "<tr><th align='left'>Habit</th><th align='center'>Frequency</th><th align='center'>Streak</th><th align='center'>Points</th></tr>"
            for habit in habits:
                habit_list += "<tr>"
                habit_list += f"<td>{habit.name}</td>"
                habit_list += f"<td align='center'>{habit.frequency} day{'s' if habit.frequency > 1 else ''}</td>"
                habit_list += f"<td align='center'>{habit.streak}</td>"
                habit_list += f"<td align='center'>{habit.points}</td>"
                habit_list += "</tr>"
            habit_list += "</table>"
            self.habit_list.setHtml(habit_list)

    def show_quote(self):
        quote = self.quotes.get_quote()
        self.quote_label.setText(f"Motivational Quote of the Day: '{quote}'")

    def get_habit_list(self):
        habits = self.db.get_all_habits()
        if not habits:
            self.habit_list.setText("You have no habits.")
        else:
            habit_list = "<table>"
            habit_list += "<tr><th align='left'>Habit</th><th align='center'>Frequency</th><th align='center'>Streak</th><th align='center'>Points</th></tr>"
            for habit in habits:
                habit_list += "<tr>"
                habit_list += f"<td>{habit.name}</td>"
                habit_list += f"<td align='center'>{habit.frequency} day{'s' if habit.frequency > 1 else ''}</td>"
                habit_list += f"<td align='center'>{habit.streak}</td>"
                habit_list += f"<td align='center'>{habit.points}</td>"
                habit_list += "</tr>"
            habit_list += "</table>"
            self.habit_list.setHtml(habit_list)
        return habit_list

    def run(self):
        self.db = Database("habits.db")
        self.tracker = HabitTracker()
        self.quotes = MotivationalQuotes()
        self.show_quote()
        self.habit_list.setText(self.get_habit_list())
        self.show()

if __name__ == "__main__":
    app = QApplication([])
    window = HabitTrackerWindow()
    window.run()
    app.exec_()