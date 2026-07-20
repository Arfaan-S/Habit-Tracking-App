from habit import Habit
from storage import HabitDB
from datetime import datetime
from analytics import *

"""defining Main menu as function so it can reused again and again for Command line interface"""
db = HabitDB()

def print_all_habits():
      all_habits = db.get_all_habits()
      table_width = 100  # Increased width to accommodate the new column

      print("\n" + "=" * table_width)
      print("📋 YOUR HABITS".center(table_width))
      print("=" * table_width)

      if all_habits:
            # Added 'Created' to the header row
            print(f"{'ID':<5} | {'Habit Name':<20} | {'Created':<12} | {'Deadline':<12} | {'Current Streak':<15} | {'Best Streak':<15}")
            print("-" * table_width)

            for h in all_habits:
                  # Added {str(h.date_of_creation):<12} to fit under the new header
                  print(f"[  {h.habit_id:<3}] | {h.name:<20} | {str(h.date_of_creation):<12} | {str(h.deadline):<12} | 🔥 {h.current_streak_count:<12} | 🏆 {h.highest_streak_count:<12}")
                  # Sub-line for additional details
                  print(f"{'':<5}   └─ Prev deadline: {h.previous_deadline} | Checked off: {h.checkoff}\n")
      else:
            # Adjusted spacing to keep the empty message centered in the wider table
            print(" " * 32 + "🍃 No habits found. It's empty here!")
      print("=" * table_width + "\n")

def main_menu():
      print("\n" + "╭─────────────────────────────╮")
      print("│         MAIN MENU           │")
      print("├─────────────────────────────┤")
      print("│  [1] 📋 List of All Habits  │")
      print("│  [2] ✅ Checkoff a Habit    │")
      print("│  [3] ➕ Create a new Habit  │")
      print("│  [4] ❌ Delete a Habit      │")
      print("│  [5] 📊 Analytics           │")
      print("│  [6] 🚪 Exit                │")
      print("╰─────────────────────────────╯")

def analytics_menu():
      print("\n" + "╭───────────────────────────────────────────────╮")
      print("│               ANALYTICS MENU                  │")
      print("├───────────────────────────────────────────────┤")
      print("│  [1] 📅 Habits by Periodicity                 │")
      print("│  [2] 🏆 Longest Streak (All Habits)           │")
      print("│  [3] 🎯 Longest Streak (Specific Habit)       │")
      print("│  [4] 🔥 Current Streaks                       │")
      print("│  [5] ⚠️ Most Struggled Habits (Last 30 Days)  │")
      print("│  [6] ⬅️  Back to Main Menu                    │")
      print("╰───────────────────────────────────────────────╯")

#Functions

# function to check if the deadline is missed you
# function to check if the deadline is missed you
def check_for_overdue() -> None:
      """
          Scans all habits and updates the status of those past their deadline.
          Fast-forwards the deadline, logs a missed record, and resets the streak.
      """

      # Evaluate 'today' exactly once to prevent midnight-rollover bugs
      # and avoid unnecessary repeated function calls in the loop.
      today = datetime.today().date()

      for habit in db.get_all_habits():
            if today <= habit.deadline:
                  continue
            if today > habit.deadline:

                  habit.checkoff_update(False)

                  # Fast-forward the deadline until it surpasses today
                  while today > habit.deadline:
                        habit.Calculate_Deadline()

                  habit.Record_update(False)
                  habit.update_current_streak_count(0)

                  db.update_habit(habit)

def reset_checkoff()-> None:
      """
          Resets the checkoff status for habits that were completed
          but have now passed their previous deadline.
      """

      # Evaluate 'today' once outside the loop for performance and consistency
      today = datetime.today().date()

      for habit in db.get_all_habits():
            # Guard clause: skip habits that haven't passed their deadline
            # or are already unchecked
            if today <= habit.previous_deadline or not habit.checkoff:
                  continue

            if today > habit.previous_deadline and habit.checkoff == True:
                  habit.checkoff_update(False)
                  db.update_habit(habit)

def menu()-> None:
      """
          Main entry point for the application.
          Handles the primary CLI loop and routes user input to the correct actions.
      """
      #inserting mock data
      db.insert_mock_data()

      # Run initial startup checks
      check_for_overdue()
      reset_checkoff()
      print_all_habits()

      # Use an infinite loop with 'break'
      while True:
            main_menu()
            choice = input("Enter your choice: ")

            if choice == "1":
                  print_all_habits()
                  input("\nPress Enter to continue...")

            elif choice == "2":
                  #checking off the habit and updating the nessecary properties of habit
                  print_all_habits()
                  habit_id_input = input("Please the id of the habit you want to cheak off")

                  #To avoid value error try method is used
                  try:
                        habit_id_input = int(habit_id_input)
                        specific_habit = db.get_habit_by_id(habit_id_input)

                        if specific_habit:

                              if specific_habit.checkoff:
                                    print(f"you have already done this habit will be avaliable from {specific_habit.previous_deadline}.")
                              else:
                                    specific_habit.checkoff_update(True)
                                    specific_habit.Record_update(True)

                                    new_streak = specific_habit.current_streak_count + 1
                                    specific_habit.update_current_streak_count(new_streak)

                                    if new_streak > specific_habit.highest_streak_count:
                                          specific_habit.update_highest_streak_count(new_streak)

                                    specific_habit.Calculate_Deadline()
                                    db.update_habit(specific_habit)
                        else:
                              print("Habit not found, try again with correct Habit ID")
                        input("please click enter to continue")
                  except ValueError:
                        print("Invalid input please try again.")
                        input("please click enter to continue")

            elif choice == "3":
                  # Adding new Habit
                  print("enter the following details please:")
                  name = input("Enter the name of the habit: ")
                  description = input("Enter the description of the habit: ")
                  periodicity = input("Enter the periodicity of the habit: ").upper()

                  if periodicity not in {"D", "W"}:
                        new_habit = Habit(name, description, periodicity)
                        db.save_habit(new_habit)
                        print(f"Habit {new_habit.name} has been created successfully.")
                  else:
                        print("Invalid input please try again.")

                  input("please click enter to continue")

            elif choice == "4":
                  #deleting the habit
                  print_all_habits()
                  try:
                        habit_id = int(input("Enter the id of the habit that you want to delete: "))
                        db.delete_habit(habit_id)
                  except ValueError:
                        print("invalid input please try again.")
                  input("please click enter to continue")

            elif choice == "5":
                  # Sub-menu loop for analytics
                  while True:
                        analytics_menu()
                        analytics_choice = input("Enter your choice: ")

                        if analytics_choice == "1":
                              print("Habit with daily periodicity or week  periodicity")
                              user_response = str(input("enter D for daily periodicity or W for week periodicity:\n")).upper()
                              habits_with_same_period(user_response)
                              input("please click enter to continue...")

                        elif analytics_choice == "2":
                              max_streak, habit_max_streak = longest_streak_of_all_habits()
                              print(f"{habit_max_streak} has the highest streak of {max_streak}")
                              input("please click enter to continue...")

                        elif analytics_choice == "3":
                              print_all_habits()
                              try:
                                    target_id = int(input("enter ID of the habit:\n"))
                                    longest_streak_of_specified_habit(target_id)
                                    input("please click enter to continue...")
                              except ValueError:
                                    print("please enter valid input")
                                    input("please click enter to continue...")

                        elif analytics_choice == "4":
                              current_streak_of_all_habits()
                              input("please click enter to continue...")

                        elif analytics_choice == "5":
                              struggling_Habit()
                              input("please click enter to continue...")

                        elif analytics_choice == "6":
                              break # Exits the analytics loop and returns to the main loop

                        else:
                              print("please enter valid input")
                              input("please click enter to continue")

            elif choice == "6":
                  break # Exits the main loop, terminating the program
            else:
                  print("please enter a valid choice")
                  input("please click enter to continue")


if __name__ == "__main__":
      menu()