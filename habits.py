from datetime import datetime

class Habit:
    def __init__(self, name, frequency):
        self.name = name
        self.frequency = frequency
        self.last_checked = None
        self.streak = 0
        self.points = 0

    def check(self):
        today = datetime.today().date()

        if self.last_checked is None or (today - self.last_checked).days >= self.frequency:
            self.streak += 1
            self.last_checked = today

            if self.frequency == 1 and self.streak % self.frequency == 0:
                self.points += 1
            elif self.frequency == 7 and self.streak % self.frequency == 0:
                self.points += 1

            return True

        else:
            self.streak = 0
            return False