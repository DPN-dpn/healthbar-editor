import tkinter as tk
from tkinter import ttk
from model.treeview_model import TreeViewModel

class MatrixTreeView(ttk.Treeview):
    def __init__(self, master, model: TreeViewModel, **kwargs):
        self.model = model
        super().__init__(master, columns=self.model.get_columns(), show='headings', selectmode='none', **kwargs)
        self._setup_columns()
        self._load_rows()

    def _setup_columns(self):
        for col in self.model.get_columns():
            self.heading(col, text=col)
            self.column(col, width=60, anchor='center')

    def _load_rows(self):
        for row in self.model.get_rows():
            self.insert("", "end", values=row)

    def add_row(self, values=None):
        self.model.add_row(values)
        self.insert("", "end", values=values if values else ["" for _ in self.model.get_columns()])

    def add_column(self, col_name):
        self.model.add_column(col_name)
        self["columns"] = self.model.get_columns()
        self.heading(col_name, text=col_name)
        self.column(col_name, width=60, anchor='center')
        # 기존 행에도 빈 값 추가
        for idx, item in enumerate(self.get_children("")):
            values = list(self.item(item, "values"))
            values.append("")
            self.item(item, values=values)
