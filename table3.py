from tkinter import messagebox
import customtkinter as ctk
import custom_treeview as ctv
from sql_connection import connection, cursor


class Table3(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sort_function = ctv.sort_function

        self.treeview_struktur = ctv.CustomTreeView(self, columns=("column1", "column2", "column3", "column4"))

        self.tree_scroll = ctk.CTkScrollbar(self, command=self.treeview_struktur.yview)
        self.tree_scroll.grid(row=0, column=0, sticky="nse", padx=(0, 40), pady=(35, 20))

        self.treeview_struktur.configure(yscrollcommand=self.tree_scroll.set)

        self.treeview_struktur.heading("#0", text="Item")
        self.treeview_struktur.heading("column1", text="Vorname",
                                       command=lambda: self.sort_function("column1", self.treeview_struktur, False))
        self.treeview_struktur.heading("column2", text="Nachname",
                                       command=lambda: self.sort_function("column2", self.treeview_struktur, False))
        self.treeview_struktur.heading("column3", text="Abteilung",
                                       command=lambda: self.sort_function("column3", self.treeview_struktur, False))
        self.treeview_struktur.heading("column4", text="Vorgesetzter",
                                       command=lambda: self.sort_function("column4", self.treeview_struktur, False))

        self.treeview_struktur.column("#0", width=0, minwidth=0, stretch=False)
        self.treeview_struktur.column("column1", width=220)
        self.treeview_struktur.column("column2", width=220)
        self.treeview_struktur.column("column3", width=200)
        self.treeview_struktur.column("column4", width=250)

        self.treeview_struktur.grid(row=2, column=0, padx=(15, 0), columnspan=8)

        self.treeview_struktur.bind("<Double-1>", self.clicker_table_3)

    def third_table_funktion(self):

        self.grid(row=1, column=0, sticky="nsew", columnspan=3)
        self.treeview_struktur.delete(*self.treeview_struktur.get_children())
        self.treeview_struktur.grid_forget()

        table3_values = cursor.execute(f'''SELECT vorname, nachname, abteilung, vorgesetzer FROM users''')
        table3_values_list = [row for row in table3_values]

        for count, record in enumerate(table3_values_list):
            tag = "even" if count % 2 == 0 else "odd"
            self.treeview_struktur.insert("", "end", iid=count, tags=tag,
                                          values=(record[0], record[1], record[2], record[3]))

        self.treeview_struktur.grid(row=0, column=0, sticky="nsew", pady=(35, 20), padx=40)
        self.sort_function("column1", self.treeview_struktur, False)

    def clicker_table_3(self, event):

        self.dialog_table3 = ctk.CTkToplevel(self)
        self.dialog_table3.geometry("260x290+1200+450")
        self.dialog_table3.resizable(False, False)
        self.dialog_table3.grab_set()
        self.dialog_table3.grid_columnconfigure(0, weight=1)
        self.dialog_table3.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.dialog_table3, text="Vorname").grid(row=0, column=0, pady=(16, 4), sticky="e")
        ctk.CTkLabel(self.dialog_table3, text="Nachname").grid(row=1, column=0, pady=4, sticky="e")
        ctk.CTkLabel(self.dialog_table3, text="Abteilung").grid(row=2, column=0, pady=4, sticky="e")
        ctk.CTkLabel(self.dialog_table3, text="Vorgesetzter").grid(row=3, column=0, pady=4, sticky="e")

        self.vorname_table3 = ctk.CTkEntry(self.dialog_table3)
        self.vorname_table3.grid(row=0, column=1, pady=(16, 4))
        self.nachname_table3 = ctk.CTkEntry(self.dialog_table3)
        self.nachname_table3.grid(row=1, column=1, pady=4)
        self.abteilung_table3 = ctk.CTkEntry(self.dialog_table3)
        self.abteilung_table3.grid(row=2, column=1, pady=4)
        self.vorgesetzter_table3 = ctk.CTkEntry(self.dialog_table3)
        self.vorgesetzter_table3.grid(row=3, column=1, pady=4)

        self.vorname_table3.bind("<Return>", self.enter_click)
        self.nachname_table3.bind("<Return>", self.enter_click)
        self.abteilung_table3.bind("<Return>", self.enter_click)
        self.vorgesetzter_table3.bind("<Return>", self.enter_click)

        self.selected_table3 = self.treeview_struktur.focus()
        self.values_table3 = self.treeview_struktur.item(self.selected_table3, 'values')

        self.dialog_table3.title(f"{self.values_table3[0]} {self.values_table3[1]}")

        self.vorname_table3.insert(0, self.values_table3[0])
        self.nachname_table3.insert(0, self.values_table3[1])
        self.abteilung_table3.insert(0, self.values_table3[2])
        self.vorgesetzter_table3.insert(0, self.values_table3[3])

        self.confirm_button_table3 = ctk.CTkButton(self.dialog_table3, text="OK",
                                                   command=self.update_record_table_3).grid(row=5, column=1,
                                                                                            pady=(30, 4))

        self.delete_button_table3 = ctk.CTkButton(self.dialog_table3, text="Löschen", fg_color="#C52233",
                                                  hover_color="#F31B31",
                                                  command=self.delete_command_table3).grid(row=6, column=1, pady=4)

    def enter_click(self, event):
        self.update_record_table_3()

    def update_record_table_3(self):
        self.treeview_struktur.item(self.selected_table3, text="",
                                    values=(self.vorname_table3.get(),
                                            self.nachname_table3.get(),
                                            self.abteilung_table3.get(),
                                            self.vorgesetzter_table3.get()))

        cursor.execute(f'''UPDATE users SET vorname = "{self.vorname_table3.get()}",
                                            nachname = "{self.nachname_table3.get()}",
                                            abteilung = "{self.abteilung_table3.get()}",
                                            vorgesetzer = "{self.vorgesetzter_table3.get()}"
                                            WHERE vorname = "{self.values_table3[0]}"
                                            AND nachname = "{self.values_table3[1]}"
                                            AND abteilung = "{self.values_table3[2]}"
                                            AND vorgesetzer = "{self.values_table3[3]}"''')

        cursor.execute(f'''UPDATE inventur SET username = "{self.vorname_table3.get()}",
                                               nachname = "{self.nachname_table3.get()}"
                                               WHERE username = "{self.values_table3[0]}"
                                               AND nachname = "{self.values_table3[1]}"''')
        connection.commit()

        self.dialog_table3.destroy()

    def delete_command_table3(self):
        delete = messagebox.askyesno("Bitte bestätigen",
                                     f"Sind Sie sicher, dass Sie den Mitarbeiter "
                                     f"{self.values_table3[0]} {self.values_table3[1]} löschen möchten?")

        if delete:
            cursor.execute(f'''DELETE FROM users WHERE vorname = "{self.vorname_table3.get()}"
                               AND nachname = "{self.nachname_table3.get()}"
                               AND abteilung = "{self.abteilung_table3.get()}"
                               AND vorgesetzer = "{self.vorgesetzter_table3.get()}"''')
            connection.commit()

            self.treeview_struktur.delete(self.selected_table3)
            self.dialog_table3.destroy()
        else:
            pass
