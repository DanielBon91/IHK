from datetime import date
from tkinter import messagebox
import customtkinter as ctk
import custom_treeview as ctv
from PIL import Image
from sql_connection import connection, cursor

date_today = date.today().strftime("%d.%m.%Y")

class Table2(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.sort_function = ctv.sort_function

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.image_return = ctk.CTkImage(Image.open("images/return.png"), size=(35, 35))

        self.treeview_inventar = ctv.CustomTreeView(self, columns=(
            "column1", "column2", "column3", "column4", "column5", "column6", "column7"))

        self.tree_scroll_invent = ctk.CTkScrollbar(self, command=self.treeview_inventar.yview)
        self.tree_scroll_invent.grid(row=0, column=0, sticky="nse", padx=(0, 40), pady=(35, 20))

        self.treeview_inventar.configure(yscrollcommand=self.tree_scroll_invent.set)

        self.treeview_inventar.heading("#0", text="Item")
        self.treeview_inventar.heading("column1", text="Vorname",
                                       command=lambda: self.sort_function("column1", self.treeview_inventar, False))
        self.treeview_inventar.heading("column2", text="Nachname",
                                       command=lambda: self.sort_function("column2", self.treeview_inventar, False))
        self.treeview_inventar.heading("column3", text="Artikel",
                                       command=lambda: self.sort_function("column3", self.treeview_inventar, False))
        self.treeview_inventar.heading("column4", text="Hersteller",
                                       command=lambda: self.sort_function("column4", self.treeview_inventar, False))
        self.treeview_inventar.heading("column5", text="Model",
                                       command=lambda: self.sort_function("column5", self.treeview_inventar, False))
        self.treeview_inventar.heading("column6", text="Seriennummer",
                                       command=lambda: self.sort_function("column6", self.treeview_inventar, False))
        self.treeview_inventar.heading("column7", text="Bemerkung",
                                       command=lambda: self.sort_function("column7", self.treeview_inventar, False))

        self.treeview_inventar.column("#0", width=0, minwidth=0, stretch=False)
        self.treeview_inventar.column("column1", width=130)
        self.treeview_inventar.column("column2", width=130)
        self.treeview_inventar.column("column3", width=180)
        self.treeview_inventar.column("column4", width=120)
        self.treeview_inventar.column("column5", width=190)
        self.treeview_inventar.column("column6", width=169)
        self.treeview_inventar.column("column7", width=190)

        self.treeview_inventar.bind("<Double-1>", self.clicker_table_2)

        self.return_button = ctk.CTkButton(self, width=300, height=70, corner_radius=7,
                                           text="Rückgabe machen", image=self.image_return,
                                           fg_color="#328E3D", hover_color="#399E5A",
                                           font=ctk.CTkFont(size=21, weight="bold"),
                                           command=self.return_function).grid(row=1, column=0, padx=40, pady=25,
                                                                              sticky="w")

        self.search = ctk.CTkEntry(self, placeholder_text="Suchen...", corner_radius=7, width=200)
        self.search.grid(row=1, column=0, padx=15, pady=25)
        self.search.bind("<KeyRelease>", self.search_funktion_event)

    def second_table_function(self):
        self.grid(row=1, column=0, sticky="nsew", columnspan=3)

        self.treeview_inventar.delete(*self.treeview_inventar.get_children())
        self.treeview_inventar.grid_forget()

        table2_values_sql = cursor.execute(f'''SELECT username, nachname, artikel, hersteller, model, sn, bemerkung 
                                               FROM inventur
                                               WHERE username LIKE "%{self.search.get()}%"''')
        table2_values_list = [row for row in table2_values_sql]

        for count, record in enumerate(table2_values_list):
            tag = "even" if count % 2 == 0 else "odd"
            self.treeview_inventar.insert("", "end", iid=count, tags=tag,
                                          values=(record[0], record[1], record[2], record[3], record[4], record[5],
                                                  record[6]))

        self.treeview_inventar.grid(row=0, column=0, sticky="nsew", pady=(35, 20), padx=40)
        self.sort_function("column1", self.treeview_inventar, False)

    def search_funktion_event(self, event):
        self.second_table_function()

    def clicker_table_2(self, event):

        self.dialog_table2 = ctk.CTkToplevel(self)
        self.dialog_table2.geometry("260x290+1200+450")
        self.dialog_table2.resizable(False, False)
        self.dialog_table2.grab_set()
        self.dialog_table2.grid_columnconfigure(0, weight=1)
        self.dialog_table2.grid_columnconfigure(1, weight=1)

        self.artikel_table2_label = ctk.CTkLabel(self.dialog_table2, text="Artikel").grid(row=0, column=0, pady=(16, 4),
                                                                                          sticky="e")
        self.hersteller_table2_label = ctk.CTkLabel(self.dialog_table2, text="Hersteller").grid(row=1, column=0, pady=4,
                                                                                                sticky="e")
        self.model_table2_label = ctk.CTkLabel(self.dialog_table2, text="Model").grid(row=2, column=0, pady=4,
                                                                                      sticky="e")
        self.sn_table2_label = ctk.CTkLabel(self.dialog_table2, text="Seriennummer").grid(row=3, column=0, pady=4,
                                                                                          sticky="e")
        self.bemerkung_table2_label = ctk.CTkLabel(self.dialog_table2, text="Bemerkung").grid(row=4, column=0, pady=4,
                                                                                              sticky="e")

        self.artikel_table2 = ctk.CTkEntry(self.dialog_table2)
        self.artikel_table2.grid(row=0, column=1, pady=(16, 4))
        self.hersteller_table2 = ctk.CTkEntry(self.dialog_table2)
        self.hersteller_table2.grid(row=1, column=1, pady=4)
        self.model_table2 = ctk.CTkEntry(self.dialog_table2)
        self.model_table2.grid(row=2, column=1, pady=4)
        self.sn_table2 = ctk.CTkEntry(self.dialog_table2)
        self.sn_table2.grid(row=3, column=1, pady=4)
        self.bemerkung_table2 = ctk.CTkEntry(self.dialog_table2)
        self.bemerkung_table2.grid(row=4, column=1, pady=4)

        self.artikel_table2.bind("<Return>", self.enter_click)
        self.hersteller_table2.bind("<Return>", self.enter_click)
        self.model_table2.bind("<Return>", self.enter_click)
        self.sn_table2.bind("<Return>", self.enter_click)
        self.bemerkung_table2.bind("<Return>", self.enter_click)

        self.selected_table2 = self.treeview_inventar.focus()
        self.values_table2 = self.treeview_inventar.item(self.selected_table2, 'values')

        self.dialog_table2.title(f"{self.values_table2[0]} {self.values_table2[1]}")

        self.artikel_table2.insert(0, self.values_table2[2])
        self.hersteller_table2.insert(0, self.values_table2[3])
        self.model_table2.insert(0, self.values_table2[4])
        self.sn_table2.insert(0, self.values_table2[5])
        self.bemerkung_table2.insert(0, self.values_table2[6])

        ctk.CTkButton(self.dialog_table2, text="OK", command=self.update_record_table_2).grid(row=5, column=1,
                                                                                              pady=(30, 4))

    def enter_click(self, event):
        self.update_record_table_2()

    def update_record_table_2(self):
        self.treeview_inventar.item(self.selected_table2,
                                    values=(self.values_table2[0], self.values_table2[1],
                                            self.artikel_table2.get(),
                                            self.hersteller_table2.get(),
                                            self.model_table2.get(),
                                            self.sn_table2.get(),
                                            self.bemerkung_table2.get()))

        cursor.execute(f'''UPDATE inventur SET artikel = "{self.artikel_table2.get()}",
                           hersteller = "{self.hersteller_table2.get()}",
                           model = "{self.model_table2.get()}",
                           sn = "{self.sn_table2.get()}",
                           bemerkung = "{self.bemerkung_table2.get()}"
                           WHERE artikel = "{self.values_table2[2]}"
                           AND hersteller = "{self.values_table2[3]}"
                           AND model = "{self.values_table2[4]}"
                           AND sn = "{self.values_table2[5]}"
                           AND bemerkung = "{self.values_table2[6]}"
                           ''')
        connection.commit()

        self.dialog_table2.destroy()

    def return_function(self):

        return_confirm = messagebox.askyesno("Bitte bestätigen", "Sind Sie sicher?")

        if return_confirm:
            for rows in self.treeview_inventar.selection():

                cursor.execute(f'''INSERT INTO lager (artikel, hersteller, model, sn, bemerkung, date)
                                   SELECT "{self.treeview_inventar.item(rows, 'values')[2]}",
                                          "{self.treeview_inventar.item(rows, 'values')[3]}",
                                          "{self.treeview_inventar.item(rows, 'values')[4]}",
                                          "{self.treeview_inventar.item(rows, 'values')[5]}",
                                          "{self.treeview_inventar.item(rows, 'values')[6]}",
                                          "{date_today}"
                                   FROM inventur
                                   WHERE artikel = "{self.treeview_inventar.item(rows, 'values')[2]}" 
                                   AND hersteller = "{self.treeview_inventar.item(rows, 'values')[3]}"
                                   AND model = "{self.treeview_inventar.item(rows, 'values')[4]}"
                                   AND sn = "{self.treeview_inventar.item(rows, 'values')[5]}"
                                   ''')
                cursor.execute(f'''DELETE FROM inventur 
                                   WHERE artikel = "{self.treeview_inventar.item(rows, 'values')[2]}" 
                                   AND hersteller = "{self.treeview_inventar.item(rows, 'values')[3]}"
                                   AND model = "{self.treeview_inventar.item(rows, 'values')[4]}"
                                   AND sn = "{self.treeview_inventar.item(rows, 'values')[5]}"''')

                #cursor.execute(f'''UPDATE inventur SET username = "lager", nachname = "lager"
                #                   WHERE artikel = "{self.treeview_inventar.item(rows, 'values')[2]}"
                #                   AND hersteller = "{self.treeview_inventar.item(rows, 'values')[3]}"
                #                   AND model = "{self.treeview_inventar.item(rows, 'values')[4]}"
                #                   AND sn = "{self.treeview_inventar.item(rows, 'values')[5]}"''')
                connection.commit()

        else:
            pass

        self.second_table_function()


