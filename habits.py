from datetime import date


class Habit:
    def __init__(self, name, frequency, target_streak):
        self.name = name
        self.frequency = frequency
        self.target_streak = target_streak
        self.last_checked = None
        self.streak = 0
        self.points = 0

    def check(self):
        today = date.today()

        # If habit has never been checked or has not been checked in frequency days
        if self.last_checked is None or (today - self.last_checked).days >= self.frequency:
            self.streak += 1
            self.last_checked = today

            # Increment points based on streak length
            if self.streak % self.frequency == 0:
                streak_multiple = self.streak // self.frequency
                if streak_multiple <= 5:
                    self.points += streak_multiple
                else:
                    self.points += 5

            # Check for bonus points
            if self.streak > self.target_streak:
                bonus_points = self.streak - self.target_streak
                self.points += bonus_points

            return True

        else:
            # Reset streak and deduct points for missed days
            missed_days = (today - self.last_checked).days - self.frequency
            if missed_days > 0:
                self.streak = 0
                penalty_points = missed_days
                if penalty_points > self.points:
                    self.points = 0
                else:
                    self.points -= penalty_points

            return False
