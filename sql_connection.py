import sqlite3

try:
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    print("connect")
except sqlite3.Error as e:
    print(f"Ошибка при подключении к базе данных: {e}")