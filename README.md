# 🚀 CLI Habit Tracker

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![SQLite](https://img.shields.io/badge/sqlite-3-green.svg)
![Testing](https://img.shields.io/badge/testing-pytest-yellow.svg)
![Architecture](https://img.shields.io/badge/design-OOP-orange.svg)

A professional, robust Command Line Interface (CLI) application designed to help users build, maintain, and analyze daily and weekly habits. Engineered with clean Object-Oriented Python and persistent SQLite storage, this tool goes beyond simple checklists by providing comprehensive analytics and automated deadline management.

## ✨ Features

* **Interactive CLI:** A user-friendly, modular command-line interface for seamless navigation.
* **Smart Deadline Management:** Automatically calculates and fast-forwards deadlines, gracefully handling missed habits and streak resets.
* **Advanced Analytics Engine:** Track your progress with deep insights:
  * Overall longest streaks and current streaks.
  * Habit-specific performance metrics.
  * Identification of "Struggling Habits" based on a rolling 30-day performance window.
* **Robust Data Persistence:** Utilizes SQLite3 with custom data adapters (JSON serialization for boolean records and ISO format for dates) to ensure state is safely maintained between sessions.
* **Comprehensive Test Suite:** Fully tested using `pytest`, featuring unit tests for the core logic, integration tests for the database layer, and mocked terminal output tests.

## 🏗️ Architecture & Tech Stack

This project is built with a focus on maintainability, separation of concerns, and robust data handling. 

* **Language:** Python 3
* **Database:** SQLite3
* **Testing:** Pytest

### Directory Structure

```text
.
├── main.py            # Primary entry point; handles the CLI loop and user interactions
├── habit.py           # Core domain model; encapsulates Habit properties and date logic
├── storage.py         # Database layer; handles all SQLite CRUD operations
├── analytics.py       # Analytics module; processes data to generate user insights
└── test_habit.py      # Comprehensive test suite (Unit, Integration, Analytics)
```

## ⚙️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/habit-tracker-cli.git
   ```
2. **Direct to Working Directory:**
    ```bash
   cd habit-tracker-cli
    ```
3. **Set up a virtual environment (Optional but Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. **Activate the virtual environment:**
   * **On macOS/Linux:**
   ```bash
    source venv/bin/activate 
    ```
   * **On Windows:**
   ```bash
    .\venv\Scripts\activate 
    ```
5. **Install testing dependencies:**
   The core application relies strictly on Python standard libraries. To run tests, install `pytest`:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

Run the application directly from your terminal:

```bash
python main.py
```

Upon your first run, the database (`habits.db`) will automatically initialize and load 4 weeks of mock data to help you explore the analytics features right away.

### Navigating the Menu
* **[1] List of All Habits:** View a cleanly formatted table of your habits, deadlines, and streaks.
* **[2] Checkoff a Habit:** Log your daily or weekly success. The system will automatically recalculate your next deadline and update your streaks.
* **[3] Create a new Habit:** Add a new Daily (`D`) or Weekly (`W`) habit to your tracking pipeline.
* **[4] Delete a Habit:** Permanently remove a habit from the database.
* **[5] Analytics:** Dive into your data to find your longest streaks, highest performing habits, and areas where you are struggling.

## 🧪 Testing

This project employs a Test-Driven Development (TDD) mindset with a robust suite of automated tests. The tests use `pytest` fixtures and `monkeypatch` to simulate database interactions and capture terminal output safely without affecting your actual `habits.db` data.

Run the test suite via:

```bash
pytest test_habit.py -v
```

## 👨‍💻 Author

**Arfaan Zameerahmed Sayyad**  
Developed as a comprehensive exercise in Object-Oriented Python, SQLite database architecture, and robust application testing. 