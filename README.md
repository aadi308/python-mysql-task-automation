# Python MySQL Task Automation

A small Python and MySQL project that manages users and tasks. The database includes a due-date validation trigger, a function for counting upcoming tasks, and a procedure that moves overdue tasks into an alert table.

## Setup

1. Install MySQL 8+ and Python 3.9+.
2. Create the database objects:
   ```bash
   mysql -u root -p < 535ProjectSpring21-a0yada05.sql
   ```
3. Create a virtual environment and install the dependency:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. Set your connection values and run the program:
   ```bash
   export MYSQL_USER=root
   export MYSQL_PASSWORD=your_password
   export MYSQL_DATABASE=task_manager
   # Optional when MySQL is not using the default port:
   export MYSQL_PORT=3306
   python cse535a0yada05Project2.py
   ```

The schema includes sample users and future-dated tasks. Run `sample_insert_test_data.sql` only if you want the additional optional records.

Credentials are read from environment variables and should never be committed.
