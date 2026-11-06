import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch


connector = types.ModuleType("mysql.connector")


class DatabaseError(Exception):
    pass


connector.Error = DatabaseError
connector.connect = MagicMock()
mysql = types.ModuleType("mysql")
mysql.connector = connector
sys.modules.setdefault("mysql", mysql)
sys.modules.setdefault("mysql.connector", connector)

module_path = Path(__file__).parents[1] / "cse535a0yada05Project2.py"
spec = importlib.util.spec_from_file_location("task_manager", module_path)
task_manager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(task_manager)


class TaskManagerTests(unittest.TestCase):
    def setUp(self):
        self.cursor = MagicMock()
        self.connection = MagicMock()

    def test_create_user_uses_parameters_and_commits(self):
        task_manager.create_user(
            self.cursor, self.connection, 8, "Sam", "Lee", "sam@example.com"
        )

        self.cursor.execute.assert_called_once_with(
            "INSERT INTO Users VALUES (%s, %s, %s, %s)",
            (8, "Sam", "Lee", "sam@example.com"),
        )
        self.connection.commit.assert_called_once()

    def test_create_task_uses_parameters_and_commits(self):
        task_manager.create_task(
            self.cursor, self.connection, 108, "Test", "2030-01-01", 8
        )

        self.cursor.execute.assert_called_once()
        self.assertEqual(self.cursor.execute.call_args.args[1], (108, "Test", "2030-01-01", 8))
        self.connection.commit.assert_called_once()

    @patch("builtins.input", side_effect=["1", "7"])
    def test_check_pending_queries_existing_user(self, _input):
        self.cursor.fetchone.side_effect = [(1,), (3,)]

        task_manager.check_pending(self.cursor)

        self.assertEqual(self.cursor.execute.call_count, 2)
        self.cursor.execute.assert_called_with("SELECT Pending(%s, %s)", (1, 7))


if __name__ == "__main__":
    unittest.main()
