import sqlite3
import pytest


def test_database_connection():
    try:
        connection = sqlite3.connect("..\my_database.db")
        cursor = connection.cursor()

        assert connection is not None
        assert cursor is not None

    except sqlite3.Error as e:
        pytest.fail(f"Fehler beim Verbinden mit der Datenbank: {e}")

    finally:
        if connection:
            connection.close()
