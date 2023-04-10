
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QSpinBox, QPushButton, QTextEdit, QMessageBox, QInputDialog, \
    QApplication, QGridLayout
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors

from habit_tracker import HabitTracker
from database import Database
from motivational_quotes import MotivationalQuotes
from datetime import datetime


class HabitTrackerWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.habit_data_window = None
        self.setWindowTitle("Habit Tracker")

        layout = QGridLayout()

        # Create a MotivationalQuotes instance and get the initial quote
        self.quotes = MotivationalQuotes()
        initial_quote = self.quotes.get_quote()

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

        target_streak_label = QLabel("Target streak:")
        layout.addWidget(target_streak_label, 2, 0)

        self.target_streak_spin = QSpinBox()
        self.target_streak_spin.setRange(1, 365)
        self.target_streak_spin.setValue(21)
        layout.addWidget(self.target_streak_spin, 2, 1)

        add_habit_button = QPushButton("Add Habit")
        add_habit_button.clicked.connect(self.add_habit)
        layout.addWidget(add_habit_button, 3, 1)

        self.habit_list = QTextEdit()
        layout.addWidget(self.habit_list, 4, 0, 1, 2)

        delete_habit_button = QPushButton("Delete Habit")
        delete_habit_button.clicked.connect(self.delete_habit)
        layout.addWidget(delete_habit_button, 5, 0)

        modify_habit_button = QPushButton("Modify Habit")
        modify_habit_button.clicked.connect(self.modify_habit)
        layout.addWidget(modify_habit_button, 5, 1)

        check_habit_button = QPushButton("Check Habit")
        check_habit_button.clicked.connect(self.check_habit)
        layout.addWidget(check_habit_button, 6, 0)

        show_data_button = QPushButton("Show Diagram")
        show_data_button.clicked.connect(self.show_habit_data)
        layout.addWidget(show_data_button, 6, 1)

        list_habits_button = QPushButton("Update List")
        list_habits_button.clicked.connect(self.list_habits)
        layout.addWidget(list_habits_button, 7, 0)

        quit_button = QPushButton("Quit")
        quit_button.clicked.connect(self.close)
        layout.addWidget(quit_button, 7, 1)

        # Set the initial value of the quote label
        self.quote_label = QLabel()
        self.quote_label.setWordWrap(True)
        self.quote_label.setText(f"Motivational Quote of the Day: '{initial_quote}'")
        layout.addWidget(self.quote_label, 8, 0, 1, 2)

        self.setLayout(layout)

    def add_habit(self):
        name = self.habit_name_edit.text()
        frequency = self.frequency_spin.value()
        target_streak = self.target_streak_spin.value()
        habit = self.tracker.add_habit(name, frequency, target_streak)
        self.db.insert_habit(habit.name, habit.frequency, habit.target_streak)
        self.habit_name_edit.setText("")
        self.frequency_spin.setValue(1)
        self.target_streak_spin.setValue(21)
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

    def show_habit_data(self):
        habits = self.db.get_all_habits()

        if not habits:
            QMessageBox.information(self, "No Habits", "You have no habits to show data for.")
            return

        # Divide habits into groups of 10
        habit_groups = [habits[i:i + 10] for i in range(0, len(habits), 10)]

        for group_idx, group in enumerate(habit_groups):
            # Create a list of habit names and their current streaks for this group
            habit_names = [habit.name for habit in group]
            habit_streaks = [habit.streak for habit in group]

            # Create a list of target streaks with None values replaced by zero
            target_streaks = [habit.target_streak if habit.target_streak else 0 for habit in group]

            # Generate a list of colors for the bars based on the number of habits
            num_habits = len(group)
            colors = list(mcolors.TABLEAU_COLORS.values())[:num_habits]

            # Create the plot
            fig, ax = plt.subplots(figsize=(10, 6))

            # Add the target streak bars
            ax.bar(range(len(group)), target_streaks, color="lightgray")

            # Add the current streak bars
            ax.bar(range(len(group)), habit_streaks, color=colors, alpha=0.7)

            # Add text labels for the current and target streaks
            for i in range(len(group)):
                ax.text(i, habit_streaks[i] + 1, str(habit_streaks[i]), ha="center", va="bottom",
                        color=colors[i])
                ax.text(i, target_streaks[i] + 1, str(target_streaks[i]), ha="center", va="bottom", color="black")

                # Add habit name vertically and inside the column
                ax.text(i, 0.5 * (habit_streaks[i] + target_streaks[i]), habit_names[i], ha="center", va="center",
                        color=colors[i], rotation=90, fontsize=10)

            # Set the x-axis labels to empty string
            ax.set_xticklabels([''] * len(group))

            # Set the y-axis limits
            ax.set_ylim([0, max(max(habit_streaks), max(target_streaks)) + 2])

            # Set the plot title and axis labels
            ax.set_title("Habit Streaks (Group {})".format(group_idx + 1))
            ax.set_ylabel("Streak")

            # Show the plot
            plt.show()
    def modify_habit(self):
        habits = self.db.get_all_habits()
        if not habits:
            QMessageBox.information(self, "No Habits", "You have no habits to modify.")
            return

        habit_names = [habit.name for habit in habits]
        choice, ok = QInputDialog.getItem(self, "Modify Habit", "Select a habit to modify:", habit_names, 0, False)
        if ok:
            habit_name = choice

            # Get new habit name from user
            new_name, ok = QInputDialog.getText(self, "Modify Habit",
                                                f"Enter the new name of the habit '{habit_name}' (leave blank to not change):",
                                                QLineEdit.Normal, habit_name)
            if ok:
                new_name = new_name.strip()
                if new_name == "":
                    new_name = habit_name

                # Get new habit frequency from user
                new_frequency, ok = QInputDialog.getInt(self, "Modify Habit",
                                                        "Enter the new frequency of the habit (leave blank to not change):",
                                                        value=habits[habit_names.index(habit_name)].frequency, min=1,
                                                        max=7)
                if ok:
                    # Get new habit target streak from user
                    new_target_streak, ok = QInputDialog.getInt(self, "Modify Habit",
                                                                "Enter the new target streak of the habit (leave blank to not change):",
                                                                value=habits[
                                                                    habit_names.index(habit_name)].target_streak, min=1,
                                                                max=365)
                    if ok:
                        self.tracker.modify_habit(habit_name, new_name, new_frequency, new_target_streak)
                        self.db.update_habit(habit_name, new_name, new_frequency, new_target_streak)
                        QMessageBox.information(self, "Habit Modified", f"The habit '{habit_name}' has been modified.")
                        self.habit_list.setText(self.get_habit_list())

    def check_habit(self):
        habits = self.db.get_all_habits()
        if not habits:
            QMessageBox.information(self, "No Habits", "You have no habits to check off.")
            return

        habit_names = [habit.name for habit in habits]
        choice, ok = QInputDialog.getItem(self, "Check Habit", "Select a habit to check off:", habit_names, 0, False)
        print(f"Choice: {choice}, ok: {ok}")
        if ok:
            habit = habits[habit_names.index(choice)]
            if habit.check(datetime.now().date()):  # add check_date argument
                self.db.update_habit_stats(habit)
                QMessageBox.information(self, "Habit Checked",
                                        f"You checked the habit '{habit.name}' on {habit.last_checked}. Your streak is now {habit.streak}. You have {habit.points} points.")
            else:
                QMessageBox.warning(self, "Habit Already Checked",
                                    f"You already checked the habit '{habit.name}' today.")
            self.habit_list.setText(self.get_habit_list())

    def list_habits(self):
        habits = self.db.get_all_habits()
        if not habits:
            self.habit_list.setText("You have no habits.")
        else:
            habit_list = "<table>"
            habit_list += "<tr><th align='left'>Habit</th><th align='center'>Frequency</th><th align='center'>Streak</th><th align='center'>Points</th><th align='center'>Target Streak</th></tr>"
            for habit in habits:
                habit_list += "<tr>"
                habit_list += f"<td>{habit.name}</td>"
                habit_list += f"<td align='center'>{habit.frequency} day{'s' if habit.frequency > 1 else ''}</td>"
                habit_list += f"<td align='center'>{habit.streak}</td>"
                habit_list += f"<td align='center'>{habit.points}</td>"
                habit_list += f"<td align='center'>{habit.target_streak if habit.target_streak else '-'}</td>"
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
            habit_list = "<table style='width:100%'>"
            habit_list += "<tr><th align='left'> Habit </th><th align='center'> Frequency </th><th align='center'> Streak </th><th align='center'> Points </th><th align='center'> Target Streak </th></tr>"
            for habit in habits:
                habit_list += "<tr>"
                habit_list += f"<td>{habit.name}</td>"
                habit_list += f"<td align='center'>{habit.frequency} day{'s' if habit.frequency > 1 else ''}</td>"
                habit_list += f"<td align='center'>{habit.streak}</td>"
                habit_list += f"<td align='center'>{habit.points}</td>"
                habit_list += f"<td align='center'>{habit.target_streak if habit.target_streak else '-'}</td>"
                habit_list += "</tr>"
            habit_list += "</table>"
            self.habit_list.setHtml(habit_list)
            self.habit_list.document().setDefaultStyleSheet("table { width: 100%; }")
        return habit_list

    def run(self):
        self.db = Database("habits.db")
        self.tracker = HabitTracker()
        self.show_quote()
        self.habit_list.setText(self.get_habit_list())
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    window = HabitTrackerWindow()
    window.run()
    app.exec_()

