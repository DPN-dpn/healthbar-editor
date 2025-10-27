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
        for idx, item in enumerate(self.get_children("")):
            values = list(self.item(item, "values"))
            values.append("")
            self.item(item, values=values)

class CenterMatrixPanel(tk.Frame):
    def __init__(self, master, log_callback=None):
        super().__init__(master, bg="#f0f0f0")
        # 레이아웃: 하단(행추가)과 우측(열추가) 고정, 좌상단(트리뷰) 확장
        self.grid_rowconfigure(0, weight=1)   # 트리뷰(확장)
        self.grid_rowconfigure(1, weight=0)   # 행추가버튼(고정)
        self.grid_columnconfigure(0, weight=1) # 트리뷰/행추가버튼(확장)
        self.grid_columnconfigure(1, weight=0) # 열추가버튼(고정)

        # 트리뷰(좌상단, 확장)
        self.tree_model = TreeViewModel()
        self.tree = MatrixTreeView(self, self.tree_model)
        self.tree.grid(row=0, column=0, sticky="nsew")

        # 열 추가 버튼(우측, 고정)
        self.btn_col_frame = tk.Frame(self, bg="#f0f0f0", width=60)
        self.btn_col_frame.grid(row=0, column=1, sticky="ns")
        self.btn_col_frame.grid_propagate(False)
        self.btn_add_col = tk.Button(
            self.btn_col_frame, text="+", font=("Arial", 16), bg="#e6e6e6", borderwidth=0, relief="flat", activebackground="#cccccc",
            command=self.add_column_event
        )
        self.btn_add_col.pack(fill=tk.BOTH, expand=True, padx=8, pady=20)

        # 행 추가 버튼(하단, 고정)
        self.btn_row_frame = tk.Frame(self, bg="#f0f0f0", height=40)
        self.btn_row_frame.grid(row=1, column=0, sticky="ew")
        self.btn_row_frame.grid_propagate(False)
        self.btn_add_row = tk.Button(
            self.btn_row_frame, text="+", font=("Arial", 16), bg="#e6e6e6", borderwidth=0, relief="flat", activebackground="#cccccc",
            command=self.add_row_event
        )
        self.btn_add_row.pack(fill=tk.BOTH, expand=True, padx=20, pady=8)

        # 빈공간(우하, 최소)
        self.empty_frame = tk.Frame(self, bg="#f0f0f0", width=60, height=40)
        self.empty_frame.grid(row=1, column=1, sticky="nsew")

        self.log_callback = log_callback

    def add_row_event(self):
        self.tree.add_row()
        if self.log_callback:
            self.log_callback("행 추가")

    def add_column_event(self):
        new_col_name = f"Col{len(self.tree_model.get_columns())+1}"
        self.tree.add_column(new_col_name)
        if self.log_callback:
            self.log_callback(f"열 추가: {new_col_name}")
