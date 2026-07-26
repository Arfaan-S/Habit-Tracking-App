from storage import HabitDB
db = HabitDB()

def print_all_habits():
    all_habits = db.get_all_habits()
    table_width = 100  # Increased width to accommodate the new column

    print("\n" + "=" * table_width)
    print("📋 YOUR HABITS".center(table_width))
    print("=" * table_width)

    if all_habits:
        # Added 'Created' to the header row
        print(
            f"{'ID':<5} | {'Habit Name':<20} | {'Created':<12} | {'Deadline':<12} | {'Current Streak':<15} | {'Best Streak':<15}")
        print("-" * table_width)

        for h in all_habits:
            # Added {str(h.date_of_creation):<12} to fit under the new header
            print(
                f"[  {h.habit_id:<3}] | {h.name:<20} | {str(h.date_of_creation):<12} | {str(h.deadline):<12} | 🔥 {h.current_streak_count:<12} | 🏆 {h.highest_streak_count:<12}")
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
    print("│  [5] ⚠️ Most Struggled Habits (Last 30 Days)   │")
    print("│  [6] ⬅️  Back to Main Menu                     │")
    print("╰───────────────────────────────────────────────╯")
