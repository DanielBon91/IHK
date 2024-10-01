import configparser
import sqlite3

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

#h = cursor.execute(f'''SELECT artikel, hersteller, model, sn, bemerkung
#            FROM inventur WHERE username IS "lager"''').fetchall()
#print(h)

#cursor.execute(f'''INSERT INTO users (vorname, nachname, abteilung, vorgesetzer)
# VALUES ("Alex", "Markstädter", "IT", "Andre Gorbunov")''')



#mitarbeiter_list = cursor.execute(f'''SELECT model, hersteller FROM inventur WHERE username != "lager"''')
#result = mitarbeiter_list
#ll = [row for row in result]
#print(ll)

cursor.execute(f"""INSERT INTO Test2 (name, user_id)
                  SELECT '{n}', 'Ali' FROM Test1
                  WHERE name = '{n}'""")
cursor.execute(f"""DELETE FROM Test1 WHERE name = '{n}'""")

#CREATE TABLE Test2 (
#    id INTEGER PRIMARY KEY,
#    name TEXT,
#    user_id INTEGER,
#    FOREIGN KEY (user_id) REFERENCES Users(id) ON UPDATE CASCADE
#);
#""")

#list_abteilung = cursor.execute('''SELECT vorname, nachname FROM users''')
#l = [(i[0].lower() + ' ' + i[1]) for i in list_abteilung.fetchall()]
#print(l)

#connection = sqlite3.connect('my_database.db')
#cursor = connection.cursor()

#cursor.execute(f'''CREATE TABLE lager (id INTEGER PRIMARY KEY, artikel TEXT, hersteller
#                    TEXT, model TEXT, sn TEXT, bemerkung TEXT, date TEXT)''')
#cursor.execute(f'''INSERT INTO abteilung_struktur (abteilung, vorgesetzer) VALUES ("Alex", "Alex")''')

#vorname = "Daniel"
#nachname = "Bondarenko"
#connection = sqlite3.connect('my_database.db')
#cursor = connection.cursor()
#abteilung = cursor.execute(f'''SELECT abteilung, vorgesetzer FROM users WHERE vorname = "Daniel" AND nachname = "Bondarenko"''').fetchone()
#print(abteilung[0], abteilung[1])


#connection = sqlite3.connect('my_database.db')
#cursor = connection.cursor()
#confirm = cursor.execute(f'''UPDATE inventur
#                             SET username = "Daniel", nachname = "Bondarenko"
#                             WHERE artikel = "Test" AND
#                                   hersteller = "Test" AND
#                                   model = "test" AND
#                                   sn = "77777"''')
#connection.commit()
#connection.close()




#for i in h.fetchall():
#    print(i)
# daten Hinzufügen
#cursor.execute('''INSERT INTO inventur
#(id INTEGER PRIMARY KEY, username, nachname, artikel, hersteller, model, sn, bemerkung, date)''')

# daten Delete
#cursor.execute('''DELETE FROM users WHERE id = 2''')


connection.commit()
connection.close()
