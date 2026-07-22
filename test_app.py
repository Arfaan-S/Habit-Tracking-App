import pytest
import os
from datetime import datetime, date, timedelta
from habit import Habit
from storage import HabitDB
import analytics


# ==========================================
# 1. FIXTURES (Setup & Teardown)
# ==========================================

@pytest.fixture
def test_db():
    """
    Creates a temporary test database, inserts the 4-week mock data,
    and cleans it up after the tests are done.
    """
    test_db_name = "test_habits.db"
    db = HabitDB(db_name=test_db_name)
    db.insert_mock_data()  # Loads your 5 predefined habits and records

    yield db  # This hands the database over to the test functions

    if hasattr(db, "conn"):
        db.conn.close()  # If your connection variable is named 'conn'
    elif hasattr(db, "close"):
        db.close()

    # Teardown: Remove the test database file after tests finish
    if os.path.exists(test_db_name):
        os.remove(test_db_name)


# ==========================================
# 2. UNIT TESTS (Testing the Habit Class)
# ==========================================

def test_habit_initialization():
    """Tests if a new habit initializes with the correct default values."""
    habit = Habit(name="Read", description="10 pages", period="D")

    assert habit.name == "Read"
    assert habit.period == "D"
    assert habit.current_streak_count == 0
    assert habit.checkoff is False
    assert habit.date_of_creation == datetime.today().date()


def test_daily_deadline_calculation():
    """Tests if a new daily habit sets the deadline to today."""
    habit = Habit(name="Code", description="Python practice", period="D")
    today = datetime.now().date()

    assert habit.deadline == today


def test_weekly_deadline_calculation():
    """Tests if a new weekly habit sets the deadline 6 days from today."""
    habit = Habit(name="Clean", description="Vacuum room", period="W")
    expected_deadline = datetime.now().date() + timedelta(days=6)

    assert habit.deadline == expected_deadline


def test_record_update():
    """Tests if updating the record correctly appends boolean values."""
    habit = Habit(name="Gym", description="Lift weights", period="D")
    habit.Record_update(True)
    habit.Record_update(False)

    assert habit.record == [True, False]


# ==========================================
# 3. INTEGRATION TESTS (Testing SQLite DB)
# ==========================================

def test_database_mock_data_insertion(test_db):
    """Tests if the mock data was inserted correctly into the database."""
    habits = test_db.get_all_habits()

    # Assert that exactly 5 predefined habits were loaded
    assert len(habits) == 5

    # Check if a specific habit from your mock data exists
    drink_water_habit = next((h for h in habits if h.name == "Drink Water"), None)
    assert drink_water_habit is not None
    assert drink_water_habit.period == "D"

    # Verify the mock record is populated (checking it has length)
    assert len(drink_water_habit.record) > 0


# ==========================================
# 4. ANALYTICS TESTS (Testing functional logic)
# ==========================================



def test_longest_streak_of_all_habits(test_db, monkeypatch):
    """Tests if the analytics module correctly finds the longest overall streak."""
    # Trick analytics.py into using our test database
    monkeypatch.setattr(analytics, "db", test_db)

    max_streak, habit_name = analytics.longest_streak_of_all_habits()

    # Based on predefined mock data, "Drink Water" has a highest streak of 7
    assert max_streak == 7
    assert habit_name == "Drink Water"


def test_habits_with_same_period_daily(test_db, monkeypatch, capsys):
    """Tests filtering habits by Daily (D) periodicity by capturing terminal print output."""
    monkeypatch.setattr(analytics, "db", test_db)

    analytics.habits_with_same_period("D")

    # capsys captures what function prints to the terminal
    captured = capsys.readouterr()

    # Verify Daily habits are printed
    assert "Drink Water" in captured.out
    assert "Read Book" in captured.out
    # Verify Weekly habits are NOT printed
    assert "Clean House" not in captured.out


def test_struggling_habit(test_db, monkeypatch, capsys):
    """Tests if the analytics correctly identifies the habit missed the most times."""
    monkeypatch.setattr(analytics, "db", test_db)

    analytics.struggling_Habit()
    captured = capsys.readouterr()

    # Based on the mock data arrays, expect a specific habit to trigger this
    assert "is the most struggling habit" in captured.out