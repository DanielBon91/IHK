import customtkinter as ctk
import custom_treeview as ctv
import os
import subprocess
from PIL import Image
from docxtpl import DocxTemplate
from sql_connection import connection, cursor
from datetime import date

date_today = date.today().strftime("%d.%m.%Y")

class SecondFrame(ctk.CTkFrame):
    """Der zweite Frame des Programms"""
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sort_function = ctv.sort_function

        # Bilderstellung
        self.image_abgabe = ctk.CTkImage(Image.open("images/abgabe.png"), size=(35, 35))
        self.image_plus = ctk.CTkImage(Image.open("images/plus.png"), size=(35, 35))
        self.image_minus = ctk.CTkImage(Image.open("images/minus.png"), size=(35, 35))
        self.image_pfeil = ctk.CTkImage(Image.open("images/pfeil.png"), size=(35, 35))
        self.word = ctk.CTkImage(Image.open("images/word.png"), size=(35, 35))

        # Erstellung der oberen Tabelle
        self.lager_table = ctv.CustomTreeView(self, columns=("column1", "column2", "column3",
                                                             "column4", "column5", "column6"))
        self.scrollbar_lager_table = ctk.CTkScrollbar(self, command=self.lager_table.yview)
        self.scrollbar_lager_table.grid(row=0, column=0, sticky="nse", padx=(0, 40), pady=(35, 20))
        self.lager_table.configure(yscrollcommand=self.scrollbar_lager_table.set)
        self.lager_table.heading("#0", text="")
        self.lager_table.heading("column1", text="Artikel",
                                 command=lambda: self.sort_function("column1", self.lager_table, False))
        self.lager_table.heading("column2", text="Hersteller",
                                 command=lambda: self.sort_function("column2", self.lager_table, False))
        self.lager_table.heading("column3", text="Model",
                                 command=lambda: self.sort_function("column3", self.lager_table, False))
        self.lager_table.heading("column4", text="Seriennummer",
                                 command=lambda: self.sort_function("column4", self.lager_table, False))
        self.lager_table.heading("column5", text="Bemerkung",
                                 command=lambda: self.sort_function("column5", self.lager_table, False))
        self.lager_table.heading("column6", text="Inv_nr",
                                 command=lambda: self.sort_function("column6", self.lager_table, False))

        self.lager_table.column("#0", width=0, minwidth=0, stretch=False)
        self.lager_table.column("column1", width=120)
        self.lager_table.column("column2", width=120)
        self.lager_table.column("column3")
        self.lager_table.column("column4")
        self.lager_table.column("column5")
        self.lager_table.column("column6")
        self.lager_table.grid(row=0, column=0, sticky="nsew", pady=(35, 20), padx=40)

        # Erstellung der unteren Tabelle
        self.empty_table = ctv.CustomTreeView(self, height=10,
                                              columns=("column1", "column2", "column3", "column4", "column5", "column6"))
        self.empty_table.heading("#0", text="")
        self.empty_table.heading("column1", text="Artikel",
                                 command=lambda: self.sort_function("column1", self.empty_table, False))
        self.empty_table.heading("column2", text="Hersteller",
                                 command=lambda: self.sort_function("column2", self.empty_table, False))
        self.empty_table.heading("column3", text="Model",
                                 command=lambda: self.sort_function("column3", self.empty_table, False))
        self.empty_table.heading("column4", text="Seriennummer",
                                 command=lambda: self.sort_function("column4", self.empty_table, False))
        self.empty_table.heading("column5", text="Bemerkung",
                                 command=lambda: self.sort_function("column5", self.empty_table, False))
        self.empty_table.heading("column6", text="Inv",
                                 command=lambda: self.sort_function("column6", self.empty_table, False))

        self.empty_table.column("#0", width=0, minwidth=0, stretch=False)
        self.empty_table.column("column1", width=120)
        self.empty_table.column("column2", width=120)
        self.empty_table.column("column3")
        self.empty_table.column("column4")
        self.empty_table.column("column5")
        self.empty_table.column("column6")
        self.empty_table.grid(row=2, column=0, sticky="nsew", padx=40, pady=20)

        # Erstellung der Tasten
        self.zuweisen_button = ctk.CTkButton(self, text="Die Waren übergebe an...", width=350, height=80,
                                             state="disabled", image=self.image_abgabe,
                                             command=self.abgabe_function, corner_radius=7,
                                             font=ctk.CTkFont(size=25))
        self.zuweisen_button.grid(row=4, column=0, pady=(0, 20))
        self.plus_button = ctk.CTkButton(self, text="", fg_color="#399E5A", corner_radius=7, hover_color="#328E3D",
                                         command=self.plus_function, image=self.image_plus, height=50)
        self.plus_button.grid(row=1, column=0, sticky="w", padx=(100, 0))
        self.minus_button = ctk.CTkButton(self, text="", fg_color="#F31B31", corner_radius=7, hover_color="#C52233",
                                          command=self.minus_function, image=self.image_minus, height=50)
        self.minus_button.grid(row=1, column=0, sticky="e", padx=(0, 100))

        self.lager_table.bind("<Double-1>", self.plus_click)
        self.empty_table.bind("<Double-1>", self.minus_click)

    def second_frame_lager_tabelle(self):
        """Die Hauptfunktion zum Anordnen und Aktualisieren von Informationen zu den Tabellen in den Frames"""
        self.grid(row=0, column=1, sticky="nsew")

        self.lager_table.delete(*self.lager_table.get_children())
        self.lager_table.grid_forget()

        lager_daten_sql = cursor.execute(f'''SELECT artikel, hersteller, model, sn, bemerkung, inv_nr
                                             FROM lager''')
        lager_daten_list = [row for row in lager_daten_sql]

        for count, record in enumerate(lager_daten_list):
            tag = "even" if count % 2 == 0 else "odd"
            self.lager_table.insert("", "end", iid=count, tags=tag,
                                    values=(record[0], record[1], record[2], record[3], record[4], record[5]))

        self.lager_table.grid(row=0, column=0, sticky="nsew", pady=(35, 20), padx=40)
        self.sort_function("column1", self.lager_table, False)

    def plus_click(self, event):
        """Funktion, die es ermöglicht, eine Zeile durch Doppelklick in die untere Tabelle hinzuzufügen"""
        self.plus_function()

    def plus_function(self):
        """Funktion zum Hinzufügen von Werten zur unteren Tabelle"""
        if len(self.empty_table.get_children()) != 10:
            for rows in self.lager_table.selection():
                self.empty_table.insert("", "end", values=(self.lager_table.item(rows, 'values')[0],
                                                           self.lager_table.item(rows, 'values')[1],
                                                           self.lager_table.item(rows, 'values')[2],
                                                           self.lager_table.item(rows, 'values')[3],
                                                           self.lager_table.item(rows, 'values')[4],
                                                           self.lager_table.item(rows, 'values')[5]))
                self.lager_table.delete(self.lager_table.selection()[0])
        else:
            self.plus_button.configure(state="disabled")

        if len(self.empty_table.get_children()) > 0:
            self.zuweisen_button.configure(state="normal")

    def minus_click(self, event):
        """Funktion, die es ermöglicht, eine Zeile durch Doppelklick aus der unteren Tabelle zu entfernen
        und sie zurück in die obere Tabelle zu verschieben"""
        self.minus_function()

    def minus_function(self):
        """Funktion zum Hinzufügen von Werten zur oberen Tabelle"""
        for rows in self.empty_table.selection():
            self.plus_button.configure(state="normal")
            self.lager_table.insert("", "end", values=(self.empty_table.item(rows, 'values')[0],
                                                       self.empty_table.item(rows, 'values')[1],
                                                       self.empty_table.item(rows, 'values')[2],
                                                       self.empty_table.item(rows, 'values')[3],
                                                       self.empty_table.item(rows, 'values')[4],
                                                       self.empty_table.item(rows, 'values')[5]))
            self.empty_table.delete(self.empty_table.selection()[0])

        if len(self.empty_table.get_children()) == 0:
            self.zuweisen_button.configure(state="disabled")

    def abgabe_function(self):
        """Funktion, die ein neues Fenster mit einer Benutzeroberfläche erstellt,
        um das Eigentum des Unternehmens an einen Mitarbeiter zu übertragen"""
        self.dialog_mitarbeiter = ctk.CTkToplevel(self)
        self.dialog_mitarbeiter.title("Bitte auswählen")
        self.dialog_mitarbeiter.geometry("800x750+1030+250")
        self.dialog_mitarbeiter.resizable(False, False)
        self.dialog_mitarbeiter.grab_set()

        self.dialog_mitarbeiter.grid_columnconfigure(0, weight=1)
        self.dialog_mitarbeiter.grid_columnconfigure(1, weight=1)

        self.dialog_mitarbeiter_label_vorname = ctk.CTkLabel(self.dialog_mitarbeiter, text="Vorname",
                                                             font=ctk.CTkFont("Calibri", weight="bold", size=25))
        self.dialog_mitarbeiter_label_vorname.grid(row=0, column=0, sticky="w", padx=(35, 0), pady=15)
        self.dialog_mitarbeiter_label_nachname = ctk.CTkLabel(self.dialog_mitarbeiter, text="Nachname",
                                                              font=ctk.CTkFont("Calibri", weight="bold", size=25))
        self.dialog_mitarbeiter_label_nachname.grid(row=0, column=1, sticky="w", padx=(35, 0), pady=15)

        mitarbeiter_list = cursor.execute(f'''SELECT DISTINCT vorname FROM users ORDER BY vorname''')
        vorname_list = [row[0] for row in mitarbeiter_list]

        self.dialog_mitarbeiter_box_vorname = ctk.CTkOptionMenu(self.dialog_mitarbeiter, width=200, values=vorname_list,
                                                                command=self.vorwahl_nachname,
                                                                font=ctk.CTkFont("Calibri", size=21, weight="bold"),
                                                                dropdown_font=ctk.CTkFont("Calibri", size=19,
                                                                                          weight="bold"))
        self.dialog_mitarbeiter_box_vorname.grid(row=1, column=0)
        self.dialog_mitarbeiter_box_vorname.set("Bitte auswählen")
        self.dialog_mitarbeiter_box_nachname = ctk.CTkOptionMenu(self.dialog_mitarbeiter, state="disabled",
                                                                 width=200,
                                                                 font=ctk.CTkFont("Calibri", size=21, weight="bold"),
                                                                 dropdown_font=ctk.CTkFont("Calibri", size=19,
                                                                                           weight="bold"))
        self.dialog_mitarbeiter_box_nachname.grid(row=1, column=1)
        self.dialog_mitarbeiter_box_nachname.set("Bitte auswählen")

    def vorwahl_nachname(self, vorname):
        """Funktion, die den Wert "Vorname" aus der vorherigen Funktion annimmt
        und eine Liste passender Nachnamen erstellt"""
        self.dialog_mitarbeiter_box_nachname.configure(state="normal")
        self.dialog_mitarbeiter_box_nachname.set("Bitte auswählen")

        nachname_mit_list = cursor.execute(f'''SELECT DISTINCT nachname FROM users 
                                               WHERE vorname = "{vorname}" ORDER BY Nachname''')
        nachname_list = [row[0] for row in nachname_mit_list]

        nachname = self.dialog_mitarbeiter_box_nachname.get()
        self.dialog_mitarbeiter_box_nachname.configure(values=nachname_list,
                                                       command=lambda nachname_get=nachname: self.confirm_function(
                                                           vorname, nachname_get))

    def confirm_function(self, vorname, nachname):
        """Funktion, die eine letzte Überprüfung der Eingabedaten ermöglicht und eine korrekte Datumsangabe
        für die Fortsetzung und Erstellung des Übergabeprotokolls erfordert"""
        ctk.CTkLabel(self.dialog_mitarbeiter, font=ctk.CTkFont(size=25, weight="bold"),
                     text=f"{vorname} {nachname} bekommt die Waren:").grid(row=2, column=0, padx=(50, 0), pady=(45, 15),
                                                                           columnspan=2, sticky="w")

        for row in self.empty_table.get_children():
            sofort_label = ' '.join(str(x) for x in self.empty_table.item(row)['values'][:4])
            ctk.CTkLabel(self.dialog_mitarbeiter, font=ctk.CTkFont(size=18),
                         text=f"- {sofort_label}").grid(column=0, columnspan=2, sticky="w", padx=(75, 0))

        ctk.CTkLabel(self.dialog_mitarbeiter, text="Übergabedatum:",
                     font=ctk.CTkFont(size=19, weight="bold")).grid(row=14, column=0, columnspan=3, sticky="w",
                                                                    padx=(60, 0), pady=20)
        self.data_entry = ctk.CTkEntry(self.dialog_mitarbeiter, height=35, placeholder_text="dd.mm.YYYY",
                                       font=ctk.CTkFont(size=19))
        self.data_entry.insert(0, date_today)
        self.data_entry.grid(row=14, column=0, sticky="w", padx=(230, 0), pady=20, columnspan=3)

        self.data_get = ctk.CTkButton(self.dialog_mitarbeiter, width=45, text="", image=self.image_pfeil,
                                      command=lambda: self.button_active(self.data_entry.get()))
        self.data_get.grid(row=14, column=0, columnspan=3)

        abteilung_info = cursor.execute(f'''SELECT abteilung, vorgesetzer FROM users 
                                            WHERE vorname = "{vorname}" 
                                            AND nachname = "{nachname}"''').fetchone()
        abteilung = abteilung_info[0]
        chef = abteilung_info[1]
        self.top_level_confirm_button = ctk.CTkButton(self.dialog_mitarbeiter, width=200, height=45,
                                                      text="Bestätigen", state="disabled",
                                                      font=ctk.CTkFont(size=21, weight="bold"),
                                                      command=lambda: self.confirm_command(vorname, nachname,
                                                                                           abteilung, chef,
                                                                                           self.data_entry.get()))
        self.top_level_confirm_button.grid(row=15, column=0, columnspan=3, pady=45, sticky="s")

    def button_active(self, date):
        """Funktion zur Überprüfung der Richtigkeit des eingegebenen Datums"""
        if len(date) == 10:
            self.top_level_confirm_button.configure(state="normal")
        else:
            pass

    def confirm_command(self, vorname, nachname, abteilung, chef, date):
        """die Abschlussfunktion zur Eintragung aller Änderungen in die Datenbank sowie
        zur Erstellung eines Dictionary für die Verwendung im Übergabeprotokoll"""
        self.top_level_confirm_button.configure(state="disabled")
        abteilung_dict = {'name': vorname,
                          'nachname': nachname,
                          'abteilung': abteilung,
                          'chef': chef}
        for value in self.empty_table.get_children():
            artikel = self.empty_table.item(value)['values'][0]
            hersteller = self.empty_table.item(value)['values'][1]
            model = self.empty_table.item(value)['values'][2]
            seriennummer = self.empty_table.item(value)['values'][3]
            bemerkung = self.empty_table.item(value)['values'][4]
            inv_nr = self.empty_table.item(value)['values'][5]

            cursor.execute(f'''INSERT INTO 
                               inventur (username, nachname, artikel, hersteller, model, sn, bemerkung, date, inv_nr)
                               SELECT "{vorname}", "{nachname}", "{artikel}", 
                               "{hersteller}", "{str(model)}", "{str(seriennummer)}", "{str(bemerkung)}", 
                               "{str(date)}", "{inv_nr}"
                               FROM lager
                               WHERE inv_nr = "{inv_nr}"''')

            cursor.execute(f'''DELETE FROM lager 
                               WHERE inv_nr = "{inv_nr}"''')
            connection.commit()

        for num, rows in enumerate(self.empty_table.get_children()):
            art_name = ' '.join(str(value) for value in self.empty_table.item(rows)['values'][:3])
            serial_num_word = self.empty_table.item(rows)['values'][3]
            abteilung_dict[f'art{num}'] = art_name
            abteilung_dict[f'sn{num}'] = serial_num_word
            abteilung_dict[f'dat{num}'] = self.data_entry.get()

        self.word_datei(abteilung_dict, vorname, nachname)
        self.empty_table.delete(*self.empty_table.get_children())

    def word_datei(self, abteilung_dict, vorname, nachname):
        """Funktion, die es ermöglicht, ein Word-Dokument für das Übergabeprotokoll auszufüllen"""
        word_datei = DocxTemplate("default_protokoll.docx")
        word_datei.render(abteilung_dict)

        count_name = 0
        files = os.listdir()
        vollname = f'{vorname}_{nachname}'

        for name in files:
            if vollname in name:
                count_name += 1

        if count_name == 0:
            file_name = f"Übergabeprotokoll_{vorname}_{nachname}.docx"
            end_word_directory = file_name
            word_datei.save(end_word_directory)
        else:
            file_name = f"Übergabeprotokoll_{vorname}_{nachname}_({count_name + 1}).docx"
            end_word_directory = file_name
            word_datei.save(end_word_directory)

        confirm_button = ctk.CTkButton(self.dialog_mitarbeiter, text="Word", image=self.word,
                                       command=lambda: self.open(end_word_directory))
        confirm_button.grid(row=16, column=0, columnspan=2)

    def open(self, end_word):
        """Funktion zum Öffnen eines Word-Dokuments"""
        subprocess.Popen(['start', end_word], shell=True)
        self.dialog_mitarbeiter.destroy()
        self.zuweisen_button.configure(state="disabled")
