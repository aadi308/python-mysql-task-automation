import os
import sys

import mysql.connector
from mysql.connector import Error


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "task_manager"),
    )


def create_user(cursor, connection, user_id, firstname, lastname, email):
    try:
        cursor.execute('INSERT INTO Users VALUES (%s, %s, %s, %s)', 
                       (user_id, firstname, lastname, email))
        connection.commit()
        print("User created.")
    except Error as e:
        print("Error in create_user:", e)


def create_task(cursor, connection, task_id, name, due_date, user_id):
    try:
        cursor.execute('INSERT INTO Tasks (taskId, Name, DueDate, UserId) VALUES (%s, %s, %s, %s)',
                       (task_id, name, due_date, user_id))
        connection.commit()
        print("Task created.")
    except Error as e:
        print("Error in create_task:", e)


def read_users(cursor):
    try:
        cursor.execute('SELECT * FROM Users')
        for row in cursor.fetchall():
            print(row)
    except Error as e:
        print("Error in read_users:", e)


def delete_user(cursor, connection, user_id):
    try:
        cursor.execute('DELETE FROM Users WHERE userId = %s', (user_id,))
        connection.commit()
        print("User deleted.")
    except Error as e:
        print("Error in delete_user:", e)


def show_overdue_tasks(cursor, connection):
    try:
        cursor.callproc('cleaning')
        connection.commit()
        cursor.execute('SELECT * FROM ALERT')
        print("Overdue Tasks in ALERT table:")
        for row in cursor.fetchall():
            print(row)
    except Error as e:
        print("Error in show_overdue_tasks:", e)

def check_pending(cursor):
    try:
        user_id = int(input("Enter user ID: "))
        days = int(input("Enter number of days: "))
        if days <= 0:
            print("Number of days must be positive.")
            return
        
        cursor.execute('SELECT COUNT(*) FROM Users WHERE userId = %s', (user_id,))
        if cursor.fetchone()[0] == 0:
            print("User ID not found.")
            return

        cursor.execute('SELECT Pending(%s, %s)', (user_id, days))
        result = cursor.fetchone()
        print(f"Pending tasks due in next {days} days: {result[0]}")
    except Error as e:
        print("Error in check_pending:", e)
    except ValueError:
        print("Invalid input.")

def main():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        read_users(cursor)
        show_overdue_tasks(cursor, connection)
        check_pending(cursor)
        return 0
    except Error as e:
        print("Connection Error:", e)
        return 1
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    sys.exit(main())

