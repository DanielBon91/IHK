import configparser
import sqlite3

config = configparser.ConfigParser()
config.read("config.ini", encoding="utf-8")
database = config['db']['db']

try:
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
except sqlite3.Error as e:
    print(f"Fehler bei Connect: {e}")