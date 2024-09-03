import sqlite3
from app import App
from custom_treeview import connection

if __name__ == "__main__":

    app = App()
    app.mainloop()
    connection.close()
    print("close")


