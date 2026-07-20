import sqlite3
import json
from datetime import datetime,timedelta, date
from typing import List, Optional

from habit import Habit

def adapt_date(val):
    """Converts a Python date object into a string for SQLite"""
    return val.isoformat()

def convert_date(val):
    """Converts a SQLite string back into a Python date object"""
    return date.fromisoformat(val.decode())

sqlite3.register_adapter(date, adapt_date)

sqlite3.register_converter("Date", convert_date)

class HabitDB:
    def __init__(self, db_name="habits.db"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        """Creates the habits table if it doesn't already exist."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS habits
                           (
                               habit_id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               name
                               TEXT
                               NOT
                               NULL,
                               description
                               TEXT,
                               period
                               TEXT,
                               date_of_creation
                               Date,
                               deadline
                               Date,
                               previous_deadline
                               Date,
                               checkoff
                               BOOLEAN,
                               record
                               TEXT,
                               current_streak_count
                               INTEGER,
                               highest_streak_count
                               INTEGER
                           )
                           ''')
            conn.commit()
        conn.close()

    def save_habit(self, habit: Habit):
        """Saves a new Habit object to the database and updates its habit_id."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            # Convert the list to a JSON string so SQL can store it
            record_json = json.dumps(habit.record)

            cursor.execute('''
                           INSERT INTO habits (name, description, period, date_of_creation, deadline, previous_deadline, checkoff, record, current_streak_count, highest_streak_count)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                           ''', (
                               habit.name, habit.description, habit.period,
                               habit.date_of_creation, habit.deadline, habit.previous_deadline,
                               habit.checkoff, record_json, habit.current_streak_count, habit.highest_streak_count
                           ))

            conn.commit()
            # Assign the newly generated SQL ID back to the Python object
            habit._habit_id = cursor.lastrowid
            print(f"Habit '{habit.name}' saved with ID: {habit.habit_id}")
        conn.close()

    def get_all_habits(self) -> List[Habit]:
        """Retrieves all habits from the database and returns them as Habit objects."""
        with sqlite3.connect(self.db_name, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
            # This allows us to access columns by name (e.g., row['name'])
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM habits")
            rows = cursor.fetchall()

            habits = []
            for row in rows:
                # Convert the JSON string back into a Python list
                record_list = json.loads(row['record'])

                # Reconstruct the Habit object
                habit = Habit(
                    habit_id=row['habit_id'],
                    name=row['name'],
                    description=row['description'],
                    period=row['period'],
                    Date_of_creation=row['date_of_creation'],
                    deadline=row['deadline'],
                    previous_deadline = row['previous_deadline'],
                    checkoff=bool(row['checkoff']),
                    record=record_list,
                    current_streak_count=row['current_streak_count'],
                    highest_streak_count=row['highest_streak_count']
                )
                habits.append(habit)
            return habits
        conn.close()

    def get_habit_by_id(self, habit_id: int) -> Optional[Habit]:
        """Retrieves a specific habit by its ID."""
        with sqlite3.connect(self.db_name, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM habits WHERE habit_id = ?", (habit_id,))
            row = cursor.fetchone()

            if row:
                record_list = json.loads(row['record'])
                return Habit(
                    habit_id=row['habit_id'],
                    name=row['name'],
                    description=row['description'],
                    period=row['period'],
                    Date_of_creation=row['date_of_creation'],
                    deadline=row['deadline'],
                    previous_deadline=row['previous_deadline'],
                    checkoff=bool(row['checkoff']),
                    record=record_list,
                    current_streak_count=row['current_streak_count'],
                    highest_streak_count=row['highest_streak_count']
                )
            return None  # Returns None if no habit was found with that ID
        conn.close()

    def update_habit(self, habit: Habit):
        """Overwrites the database row with the current state of the Habit object."""
        if habit.habit_id is None:
            print("Error: Cannot update a habit that hasn't been saved yet (no ID).")
            return

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            # Repackage the record list into JSON
            record_json = json.dumps(habit.record)

            # The UPDATE command targets the specific row using WHERE habit_id = ?
            cursor.execute('''
                           UPDATE habits
                           SET name             = ?,
                               description      = ?,
                               period           = ?,
                               date_of_creation = ?,
                               deadline         = ?,
                               previous_deadline = ?,
                               checkoff         = ?,
                               record           = ?,
                               current_streak_count  = ?,
                               highest_streak_count  = ?
                           WHERE habit_id = ?
                           ''', (
                               habit.name, habit.description, habit.period,
                               habit.date_of_creation, habit.deadline, habit.previous_deadline,
                               habit.checkoff, record_json, habit.current_streak_count,
                               habit.highest_streak_count, habit.habit_id
                           ))

            conn.commit()
            print(f"Habit ID {habit.habit_id} successfully updated in database.")
        conn.close()

    def delete_habit(self, habit_id: int) -> bool:
        """
                Deletes a habit from the database by its ID.
                Returns True if a habit was successfully deleted, False otherwise.
        """
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute('DELETE FROM habits WHERE habit_id = ?', (habit_id,))
            if cur.rowcount == 0:
                print("No habit found with that ID.")
            else:
                print(f"Successfully deleted habit with that ID.{habit_id}.")
            conn.commit()
        conn.close()

    def insert_mock_data(self):
        """Insert 5 predefined habits and 4 weeks of mock completion data."""
        with sqlite3.connect(self.db_name, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM habits")
            if cursor.fetchone()[0] > 0:
                return  # Data already exists
            now = datetime.today().date()
            creation_time = (now - timedelta(days=30))
            print(f"Creation time: {creation_time}")

            #saving pre-defined habit to database
            record_of_habit = [
                [True, True, False, True, True, True, True, True, False, True, True, True, True, True, True, True, False, True, False, False, True, True, False, False, False, True, True, False, True],
                [True, False, True, False, False, False, True, False, True, False, True, False, False, True, True, True, True, False, True, True, True, False, False, False, False, True, False, False, True],
                [False, True, True, True, True, False, False, False, True, False, True, True, True, False, False, False, True, True, False, True, False, False, False, True, False, True, True, False, False],
                [False, False, True, True, False],
                [True, True, True, True, True]
            ]

            predefined_habits = [
                ("Drink Water", "Drink 2 liters of water", "D", 1, 7),
                ("Read Book", "Read at least 15 pages", "D", 1, 4),
                ("Morning Run", "Run 5 kilometers", "D", 0, 4),
                ("Clean House", "Vacuum and wipe down surfaces", "W", 0, 2),
                ("Call Family", "Catch up with parents", "W", 5, 5)
            ]


            for i in range(5):
                delta = 1 if predefined_habits[i][2] == "D" else 7
                cal_previous_deadline = now - timedelta(days=delta)
                pre_defined_habit = Habit(predefined_habits[i][0],predefined_habits[i][1],predefined_habits[i][2], previous_deadline = cal_previous_deadline, record = record_of_habit[i], current_streak_count = predefined_habits[i][3], highest_streak_count = predefined_habits[i][4])
                self.save_habit(pre_defined_habit)

                cursor.execute('''
                            UPDATE habits
                            set date_of_creation = ?
                            where habit_id = ?
                            ''', (creation_time,pre_defined_habit.habit_id))
                conn.commit()
        conn.close()