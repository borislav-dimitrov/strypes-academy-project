import tkinter as tk
from tkinter import ttk

from model.entities.counterparty import Counterparty
from model.entities.invoices import Invoice
from model.entities.product import Product
from model.entities.transaction import Transaction
from model.entities.warehouse import Warehouse

DEFAULT_COLUMN_WIDTH_PX = 140


class TransactionItemList:
    def __init__(self, parent, items, row, col, rowspan=None, colspan=None, sticky="nsew"):
        super().__init__()
        self.parent = parent
        self.items = items
        self.item_pos_ids = None

        self.frame = ttk.Frame(self.parent)
        self.frame.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan, sticky=sticky)

        if items:
            columns = [key for key in self.items[0].__dict__.keys()]
            columns.remove("assets")
        else:
            columns = ["id", "type", "date", "counterparty", "price", "invoice"]

        self.tree = ttk.Treeview(self.frame, columns=columns, selectmode='extended', show='headings')

        # Set column width
        for column in columns:
            self.tree.heading(column, text=column.title())
            self.tree.column(column, width=DEFAULT_COLUMN_WIDTH_PX)

        self.tree.grid(row=0, column=0, sticky="nsew")

        # resize the parent window to show treeview widget
        self.tree.update_idletasks()
        self.frame.rowconfigure(0, weight=1, minsize=self.tree.winfo_height())
        self.frame.columnconfigure(0, weight=1, minsize=self.tree.winfo_width())

        # add vertical scrollbar
        vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=0, column=1, sticky="nws", padx=0)
        self.tree.configure(yscroll=vsb.set)

        # set items
        if self.items:
            self.set_items(self.items)

    def set_items(self, items):
        def set_item(item):
            values = list(val for val in item.__dict__.values() if not isinstance(val, (list, tuple)))
            for i, val in enumerate(values):
                if isinstance(val, Counterparty):
                    values[i] = f"{val.id}, {val.name}, {val.payment_nr}"
                elif isinstance(val, Invoice):
                    values[i] = f"{val.id}, Invoice #{val.number}, {val.status}"

            return self.tree.insert('', tk.END, values=tuple(values))

        if self.item_pos_ids is not None:
            self.tree.delete(*self.item_pos_ids)
        self.items = items
        self.item_pos_ids = list(map(set_item, self.items))
        self.parent.update_idletasks()
        if self.items:
            self.tree.see(self.item_pos_ids[-1])

    def get_selected_items(self):
        items = []
        for sel_item in self.tree.selection():
            items.append(self.tree.item(sel_item, 'values'))
        return items
