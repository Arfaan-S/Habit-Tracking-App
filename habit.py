import json
from datetime import datetime, timedelta, date
from typing import List, Optional

class Habit:

    """
        Represents a user's habit, tracking its schedule, streaks, and completion record.
    """

    def __init__(self, name: str, description: str, period: str,
                 habit_id: Optional[int] = None,
                 Date_of_creation: Optional[datetime] = None,
                 checkoff: bool = False,
                 deadline: Optional[datetime] = None,
                 previous_deadline: Optional[datetime] = None,
                 record: Optional[List[bool]] = None,
                 current_streak_count: Optional[int] = 0,
                 highest_streak_count: Optional[int] = 0):

        # Public attribute
        self._habit_id = habit_id

        # Protected attributes
        self._name = name
        self._description = description
        self._period = period

        # Date objects handling
        self._date_of_creation = Date_of_creation or datetime.today().date()
        self._checkoff = checkoff
        self._deadline = deadline if deadline else self.Calculate_Deadline()
        self._previous_deadline = previous_deadline if previous_deadline else self._deadline

        # History of performance
        self._record = record if record is not None else []
        self._current_streak_count = current_streak_count
        self._highest_streak_count = highest_streak_count

    def Calculate_Deadline(self) -> date:
        """
            Calculates and updates the next deadline based on the habit's periodicity.
            If this is an existing habit rolling over, it also updates the previous deadline.
        """

        today = datetime.now().date()

        is_new_habit = (self._date_of_creation == today) and not self._checkoff

        if is_new_habit:
            # Initial deadline setup
            days_to_add = 0 if self._period == "D" else 6
            self._deadline = today + timedelta(days=days_to_add)
        else:
            # Rolling over an existing deadline
            self._previous_deadline = self._deadline
            days_to_add = 1 if self._period == "D" else 7
            self._deadline = self._deadline + timedelta(days=days_to_add)

        return self._deadline

    def checkoff_update(self, checkoff: bool) -> None:
        """Updates the completion status of the habit."""
        self._checkoff = checkoff

    def Record_update(self, status: bool) -> None:
        """Appends the daily success or failure status to the tracking record."""
        self._record.append(status)

    def update_current_streak_count(self, value: int)-> None:
        """Updates the current streak counter."""
        self._current_streak_count = value

    def update_highest_streak_count(self, value: int) -> None:
        """Updates the highest recorded streak."""
        self._highest_streak_count = value

    # --- Properties to allow the Database to read private attributes ---
    @property
    def habit_id(self) -> Optional[int]:
        return self._habit_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def period(self) -> str:
        return self._period

    @property
    def date_of_creation(self) -> date:
        return self._date_of_creation

    @property
    def deadline(self) -> date:
        return self._deadline

    @property
    def previous_deadline(self) -> date:
        return self._previous_deadline

    @property
    def checkoff(self) -> bool:
        return self._checkoff

    @property
    def record(self) -> List[bool]:
        return self._record

    @property
    def current_streak_count(self) -> int:
        return self._current_streak_count

    @property
    def highest_streak_count(self) -> int:
        return self._highest_streak_count