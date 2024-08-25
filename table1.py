import customtkinter as ctk
import custom_treeview as ctv
import sqlite3
class Table1(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)

        self.treeview_lager = ctv.CustomTreeView(self, height=25, columns=(
            "column1", "column2", "column3", "column4", "column5"))

        self.tree_scroll_lager = ctk.CTkScrollbar(self, command=self.treeview_lager.yview)
        self.tree_scroll_lager.grid(row=0, column=0, sticky="nse", padx=(0,40), pady=(35, 20))

        self.treeview_lager.configure(yscrollcommand=self.tree_scroll_lager.set)

        self.treeview_lager.heading("#0", text="Item")
        self.treeview_lager.heading("column1", text="Artikel",
                                    command=lambda: self.sort_function("column1", self.treeview_lager, False))
        self.treeview_lager.heading("column2", text="Hersteller",
                                    command=lambda: self.sort_function("column2", self.treeview_lager, False))
        self.treeview_lager.heading("column3", text="Model",
                                    command=lambda: self.sort_function("column3", self.treeview_lager, False))
        self.treeview_lager.heading("column4", text="Seriennummer",
                                    command=lambda: self.sort_function("column4", self.treeview_lager, False))
        self.treeview_lager.heading("column5", text="Bemerkung",
                                    command=lambda: self.sort_function("column5", self.treeview_lager, False))

        self.treeview_lager.column("#0", width=0, minwidth=0, stretch=0)
        self.treeview_lager.column("column1", width=180)
        self.treeview_lager.column("column2", width=180)
        self.treeview_lager.column("column3", width=260)
        self.treeview_lager.column("column4", width=190)
        self.treeview_lager.column("column5", width=224)

        self.treeview_lager.bind("<Double-1>", self.clicker_table_1)

    def sort_function(self, column, table, reverse=False):
        data = [(table.set(child, column), child) for child in table.get_children()]
        data.sort(reverse=reverse)
        for index, (val, child) in enumerate(data):
            table.move(child, '', index)

        table.tag_configure("even", background='gray85')
        table.tag_configure("odd", background='white')
        for count, item in enumerate(table.get_children()):
            tag = "even" if count % 2 == 0 else "odd"
            table.item(item, tags=(tag))

    def first_table_function(self):
        self.grid(row=1, column=0, sticky="nsew", columnspan=3)

        self.treeview_lager.delete(*self.treeview_lager.get_children())
        self.treeview_lager.grid_forget()

        self.treeview_lager.tag_configure("odd", background="white")
        self.treeview_lager.tag_configure("even", background="gray85")

        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()
        table1_values = cursor.execute(f'''SELECT artikel, hersteller, model, sn, bemerkung 
                                           FROM inventur 
                                           WHERE username = "lager"''')

        table1_values_list = [row for row in table1_values]

        for count, record in enumerate(table1_values_list):
            tag = "even" if count % 2 == 0 else "odd"
            self.treeview_lager.insert("", "end", iid=count, tags=(tag),
                                       values=(record[0], record[1], record[2], record[3], record[4]))

        self.treeview_lager.grid(row=0, column=0, sticky="nsew", pady=(35, 20), padx=40)
        self.sort_function("column1", self.treeview_lager, False)

    def clicker_table_1(self, event):

        self.dialog_table1 = ctk.CTkToplevel(self)
        self.dialog_table1.geometry(f"260x290+1200+450")
        self.dialog_table1.resizable(False, False)
        self.dialog_table1.grab_set()
        self.dialog_table1.configure(background="green")
        self.dialog_table1.grid_columnconfigure(0, weight=1)
        self.dialog_table1.grid_columnconfigure(1, weight=1)

        self.artikel_table1_label = ctk.CTkLabel(self.dialog_table1, text="Artikel")
        self.artikel_table1_label.grid(row=0, column=0, pady=(16, 4), sticky="e")
        self.hersteller_table1_label = ctk.CTkLabel(self.dialog_table1, text="Hersteller")
        self.hersteller_table1_label.grid(row=1, column=0, pady=4, sticky="e")
        self.model_table1_label = ctk.CTkLabel(self.dialog_table1, text="Model")
        self.model_table1_label.grid(row=2, column=0, pady=4, sticky="e")
        self.sn_table1_label = ctk.CTkLabel(self.dialog_table1, text="Seriennummer")
        self.sn_table1_label.grid(row=3, column=0, pady=4, sticky="e")
        self.bemerkung_table1_label = ctk.CTkLabel(self.dialog_table1, text="Bemerkung")
        self.bemerkung_table1_label.grid(row=4, column=0, pady=4, sticky="e")

        self.artikel_table1 = ctk.CTkEntry(self.dialog_table1)
        self.artikel_table1.grid(row=0, column=1, pady=(16, 4))
        self.hersteller_table1 = ctk.CTkEntry(self.dialog_table1)
        self.hersteller_table1.grid(row=1, column=1, pady=4)
        self.model_table1 = ctk.CTkEntry(self.dialog_table1)
        self.model_table1.grid(row=2, column=1, pady=4)
        self.sn_table1 = ctk.CTkEntry(self.dialog_table1)
        self.sn_table1.grid(row=3, column=1, pady=4)
        self.bemerkung_table1 = ctk.CTkEntry(self.dialog_table1)
        self.bemerkung_table1.grid(row=4, column=1, pady=4)

        self.selected_table1 = self.treeview_lager.focus()

        self.values_table1 = self.treeview_lager.item(self.selected_table1, 'values')

        self.dialog_table1.title(f"{self.values_table1[0]} {self.values_table1[1]}")

        self.artikel_table1.insert(0, self.values_table1[0])
        self.hersteller_table1.insert(0, self.values_table1[1])
        self.model_table1.insert(0, self.values_table1[2])
        self.sn_table1.insert(0, self.values_table1[3])
        self.bemerkung_table1.insert(0, self.values_table1[4].strip())

        self.confirm_button_table1 = ctk.CTkButton(self.dialog_table1, text="OK", command=self.update_record_table_1)
        self.confirm_button_table1.grid(row=5, column=1,pady=(20, 4))

        self.delete_button_table1 = ctk.CTkButton(self.dialog_table1, text="Löschen", fg_color="#C52233",
                                                  hover_color="#F31B31", command=self.delete_command_table1)
        self.delete_button_table1.grid(row=6, column=1, pady=4)

    def update_record_table_1(self):
        self.treeview_lager.item(self.selected_table1, text="",
                                 values=(self.artikel_table1.get(),
                                         self.hersteller_table1.get(),
                                         self.model_table1.get(),
                                         self.sn_table1.get(),
                                         self.bemerkung_table1.get()))

        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()

        cursor.execute(f'''UPDATE inventur SET artikel = "{self.artikel_table1.get()}", 
                                               hersteller = "{self.hersteller_table1.get()}", 
                                               model="{self.model_table1.get()}", 
                                               sn = "{self.sn_table1.get()}", 
                                               bemerkung = "{self.bemerkung_table1.get()}" 
                                               WHERE artikel = "{self.values_table1[0]}"
                                               AND hersteller = "{self.values_table1[1]}" 
                                               AND model = "{self.values_table1[2]}" 
                                               AND sn = "{self.values_table1[3]}" 
                                               AND bemerkung = "{self.values_table1[4]}"''')

        connection.commit()
        connection.close()
        self.dialog_table1.destroy()

    def delete_command_table1(self):

        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()

        self.delete_table1_string = cursor.execute(
            f"""DELETE FROM inventur 
                WHERE artikel = '{self.artikel_table1.get()}' 
                AND hersteller='{self.hersteller_table1.get()}' 
                AND model='{self.model_table1.get()}' 
                AND sn ='{self.sn_table1.get()}'""")

        self.treeview_lager.delete(self.selected_table1)

        connection.commit()
        connection.close()

        self.dialog_table1.destroy()