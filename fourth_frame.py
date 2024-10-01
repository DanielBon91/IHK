import customtkinter as ctk
from PIL import Image
from sql_connection import connection, cursor


class FourthFrame(ctk.CTkFrame):
    """Der vierte Frame des Programms"""
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.grid_columnconfigure((0, 3), weight=1)
        self.grid_columnconfigure(1, minsize=145)
        self.grid_rowconfigure(0, minsize=145)

        self.users = ctk.CTkImage(Image.open("images/users.png"), size=(80, 80))
        self.word = ctk.CTkImage(Image.open("images/word.png"), size=(35, 35))

        # Label create
        self.vorname_label = ctk.CTkLabel(self, text="Vorname", font=ctk.CTkFont("Calibri", size=25, weight="bold"))
        self.vorname_label.grid(row=1, column=1, sticky="w", pady=15)
        self.nachname_label = ctk.CTkLabel(self, text="Nachname", font=ctk.CTkFont("Calibri", size=25, weight="bold"))
        self.nachname_label.grid(row=2, column=1, sticky="w", pady=15)
        self.abteilung_label = ctk.CTkLabel(self, text="Abteilung", font=ctk.CTkFont("Calibri", size=25, weight="bold"))
        self.abteilung_label.grid(row=3, column=1, sticky="w", pady=15)
        self.label_error = ctk.CTkLabel(self, text_color="red")

        # Entry create
        self.vorname_entry = ctk.CTkEntry(self, width=250, height=45, corner_radius=7,
                                          font=ctk.CTkFont("Calibri", size=23))
        self.vorname_entry.grid(row=1, column=2)
        self.nachname_entry = ctk.CTkEntry(self, width=250, height=45, corner_radius=7,
                                           font=ctk.CTkFont("Calibri", size=23))
        self.nachname_entry.grid(row=2, column=2)

        # Combo create
        list_abteilung_sql = cursor.execute('''SELECT abteilung FROM abteilung_struktur''')
        self.list_abteilung = [abt[0] for abt in list_abteilung_sql.fetchall()]
        self.abteilung_combobox = ctk.CTkComboBox(self, values=self.list_abteilung, corner_radius=7, width=250,
                                                  height=45, font=ctk.CTkFont("Calibri", size=23),
                                                  dropdown_font=ctk.CTkFont("Calibri", size=23))
        self.abteilung_combobox.set(" Bitte auswählen")
        self.abteilung_combobox.grid(row=3, column=2)

        # Button create
        self.button_confirm = ctk.CTkButton(self, text="Hinzufügen", width=235, height=65,
                                            font=ctk.CTkFont("Calibri", size=28), corner_radius=7,
                                            command=lambda: self.mitarbeiter_add(
                                                self.vorname_entry.get().strip().capitalize(),
                                                self.nachname_entry.get().strip().capitalize(),
                                                self.abteilung_combobox.get()))
        self.button_confirm.grid(row=5, column=1, columnspan=2, pady=(65, 0))

    def mitarbeiter_add(self, vorname, nachname, abteilung):
        """Neue Mitarbeiter hinzufügen"""
        abteilung_dict_sql = cursor.execute('''SELECT abteilung, vorgesetzer FROM abteilung_struktur''')
        vorgesetzter_dict = {value[0]: value[1] for value in abteilung_dict_sql.fetchall()}

        repeat_list_sql = cursor.execute('''SELECT vorname, nachname FROM users''')
        repeat_liste = [(value[0].lower() + " " + value[1].lower()) for value in repeat_list_sql.fetchall()]

        if vorname.lower() + ' ' + nachname.lower() in repeat_liste:
            self.label_error.configure(text=f"Der Mitarbeiter {vorname} {nachname}\nexistiert bereits",
                                       text_color="Yellow")
            self.label_error.grid(row=6, column=1, columnspan=2, sticky="n")
            self.after(4000, lambda: self.label_error.grid_forget())
            self.vorname_entry.delete(0, "end")
            self.nachname_entry.delete(0, "end")
            self.abteilung_combobox.set(" Bitte auswählen")

        elif len(vorname) == 0 or len(nachname) == 0 or abteilung == " Bitte auswählen":
            self.label_error.configure(text="Bitte füllen Sie alle Felder aus", text_color="red")
            self.label_error.grid(row=6, column=1, columnspan=2, sticky="n")
            self.after(4000, lambda: self.label_error.grid_forget())

        elif len(vorname) > 0 and len(nachname) > 0 and abteilung != " Bitte auswählen":
            cursor.execute(f'''INSERT INTO users (vorname, nachname, abteilung, vorgesetzer) 
                               VALUES ("{vorname}", "{nachname}", "{abteilung}", "{vorgesetzter_dict[abteilung]}")''')
            connection.commit()

            four_frame_label_hinzu = ctk.CTkLabel(self, font=ctk.CTkFont("Calibri", size=22), text_color="#9fd8cb",
                                                  justify=ctk.LEFT, image=self.users, compound="top",
                                                  text=f"\nMitarbeiter: {vorname} {nachname}"
                                                       f"\nAbteilung: {abteilung}\n"
                                                       f"Vorgesetzter: {vorgesetzter_dict[abteilung]}\n"
                                                       f"\nwurde erfolgreich hinzugefügt ✓", anchor="w")

            four_frame_label_hinzu.grid(row=6, column=1, columnspan=2, pady=(35, 0))
            self.after(4000, lambda: four_frame_label_hinzu.grid_forget())
            self.vorname_entry.delete(0, "end")
            self.nachname_entry.delete(0, "end")
            self.abteilung_combobox.set(" Bitte auswählen")
