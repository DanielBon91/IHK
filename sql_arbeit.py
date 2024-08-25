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


#list_abteilung = cursor.execute('''SELECT vorname, nachname FROM users''')
#l = [(i[0].lower() + ' ' + i[1]) for i in list_abteilung.fetchall()]
#print(l)
config = configparser.ConfigParser()
config.read("config.ini", encoding='utf-8')

werte_list = []
for werte in config['wert']["werte"].split(','):
    sub_list_wert = []
    sub_list_wert.append(werte)
    werte_list.append(sub_list_wert)


# Выводим результат
print(werte_list)

#connection = sqlite3.connect('my_database.db')
#cursor = connection.cursor()

#cursor.execute(f'''CREATE TABLE abteilung_struktur (id INTEGER PRIMARY KEY, abteilung TEXT, vorgesetzer TEXT)''')
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
