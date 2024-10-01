from app import App
from sql_connection import connection

"""Diese Datei wird ausschließlich zum Starten des Programms verwendet"""

if __name__ == "__main__":
    app = App()
    app.mainloop()
    connection.close()
