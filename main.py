from app import App
from sql_connection import connection

if __name__ == "__main__":

    app = App()
    app.mainloop()
    connection.close()


