"""all the function that are necessary for analysis are defined here"""
from typing import Tuple, Optional
from habit import Habit
from storage import HabitDB
from Main import *

db = HabitDB()


def habits_with_same_period(period:str)-> None:
    """
        Filters and displays all habits that match the specified periodicity
        (e.g., 'D' for Daily, 'W' for Weekly).
    """
    # Guard clause: Fail fast if an invalid period is provided
    if period not in {"D", "W"}:
        print("Invalid period specified. Please use 'D' or 'W' please try again.")
        return

    # Fetch from the database
    all_habits = db.get_all_habits()

    for habit in all_habits:
        if habit.period == period:
            print(f"Name of Habit is {habit.name} and it has {habit.period} periodicity.")


def longest_streak_of_all_habits() -> Tuple[int, Optional[str]]:
    """
        Iterates through all habits, prints their individual highest streaks,
        and calculates the overall maximum streak across all habits.

        Returns:
            A tuple containing the maximum streak integer and the name of the habit
            (or None if no habits exist).
    """
    all_habits = db.get_all_habits()

    # Guard clause: Handle the edge case where the database is completely empty
    if not all_habits:
        return 0, None

    max_streak = 0
    habit_name_with_max_streak = None

    for habit in all_habits:
        print(f"Longest streak of {habit.name} is {habit.highest_streak_count}\n")

        if habit.highest_streak_count > max_streak:
            max_streak = habit.highest_streak_count
            habit_name_with_max_streak = habit.name

    return max_streak, habit_name_with_max_streak


def longest_streak_of_specified_habit(habit_id: int) -> None:
    """
        Finds a specific habit by its ID and displays its highest streak.
    """
    habit = db.get_habit_by_id(habit_id)
    if habit:
        print(f"Longest streak of {habit.name} is {habit.highest_streak_count}")
        print(f"Record: {habit.record}")
    else:
        print("Habit not found.")


def current_streak_of_all_habits():
    """
        Iterates through all habits and displays their current streak.
    """
    all_habits = db.get_all_habits()

    if not all_habits:
        print("No habits found.")
        return

    for habit in all_habits:
        print(f"Current streak of {habit.name} is {habit.current_streak_count}\n")


def struggling_Habit() -> None:
    """
        Evaluates the last 30 entries of all habits to find the one
        with the highest number of missed days (False values).
    """
    all_habits = db.get_all_habits()

    if not all_habits:
        print("No habits found.")
        return

    worst_habit_name = None
    worst_habit_record = None
    max_missed_count = 0
    for habit in all_habits:
        habit_record = habit.record
        # Slicing the last 30 elements for last 30 days
        last_30_days = habit_record[-30:]
        missed_count = last_30_days.count(False)

        if missed_count > max_missed_count:
            max_missed_count = missed_count
            worst_habit_name = habit.name
            worst_habit_record = last_30_days
    # Handle the edge case where the user has perfect streaks across all habits
    if worst_habit_name is None:
        print("Great job! No struggling habits found in the last 30 days.")
    else:
        # Split the output into multiple prints for cleaner code and terminal output
        print(f"{worst_habit_name} is the most struggling habit.")
        print(f"Record for last 30 days: {worst_habit_record}")
        print(f"Habit missed {max_missed_count} times.")