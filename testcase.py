import unittest
import sqlite3
from habit_tracker import HabitTracker

class TestHabitTracker(unittest.TestCase):

    def setUp(self):
        # Set up a test database and HabitTracker object
        self.conn = sqlite3.connect('test.db')
        self.tracker = HabitTracker(self.conn)

    def test_add_habit(self):
        # Test adding a habit
        self.tracker.add_habit('Exercise', 'daily')
        habits = self.tracker.get_all_habits()
        self.assertEqual(len(habits), 1)
        self.assertEqual(habits[0]['name'], 'Exercise')
        self.assertEqual(habits[0]['frequency'], 'daily')
        self.assertEqual(habits[0]['streak'], 0)
        self.assertEqual(habits[0]['points'], 0)

    def test_delete_habit(self):
        # Test deleting a habit
        self.tracker.add_habit('Exercise', 'daily')
        self.tracker.delete_habit('Exercise')
        habits = self.tracker.get_all_habits()
        self.assertEqual(len(habits), 0)

    def test_modify_habit(self):
        # Test modifying a habit
        self.tracker.add_habit('Exercise', 'daily')
        self.tracker.modify_habit('Exercise', 'weekly')
        habits = self.tracker.get_all_habits()
        self.assertEqual(len(habits), 1)
        self.assertEqual(habits[0]['frequency'], 'weekly')

    def test_check_habit(self):
        # Test checking off a habit
        self.tracker.add_habit('Exercise', 'daily')
        self.tracker.check_habit('Exercise')
        habits = self.tracker.get_all_habits()
        self.assertEqual(len(habits), 1)
        self.assertEqual(habits[0]['streak'], 1)
        self.assertEqual(habits[0]['points'], 1)

    def tearDown(self):
        # Clean up the test database
        self.conn.close()

if __name__ == '__main__':
    unittest.main()