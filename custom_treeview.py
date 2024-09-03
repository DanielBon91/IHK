import tkinter.ttk as ttk
from tkinter.ttk import Style


def sort_function(column, table, reverse=False):
    data = [(table.set(child, column), child) for child in table.get_children()]
    data.sort(reverse=reverse)
    for index, (val, child) in enumerate(data):
        table.move(child, '', index)

    table.tag_configure("even", background='gray85')
    table.tag_configure("odd", background='white')
    for count, item in enumerate(table.get_children()):
        tag = "even" if count % 2 == 0 else "odd"
        table.item(item, tags=tag)


class CustomTreeView(ttk.Treeview):

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        Style().configure("Treeview", rowheight=35, font=("Calibri", 11))
        style = ttk.Style()
        style.map('Treeview', background=[('selected', '#347083')])
