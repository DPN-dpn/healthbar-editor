import tkinter as tk
import tkinter.ttk as ttk
from model.treeview_model import TreeViewModel

class MatrixPanel(tk.Frame):
    def __init__(self, master, log_callback=None, handler=None):
        super().__init__(master, bg="#f0f0f0")
        self.config(width=400, height=300)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)

        self.model = TreeViewModel()
        self.tree = ttk.Treeview(self, columns=self.model.get_columns(), show='headings', selectmode='none', height=15)
        self._setup_columns()
        self._load_rows()
        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.scrollbar_y.grid(row=0, column=2, sticky="ns")
        self.vpad_frame = tk.Frame(self, bg="#f0f0f0", width=8)
        self.vpad_frame.grid(row=0, column=3, sticky="ns")
        self.scrollbar_x.grid(row=2, column=0, columnspan=3, sticky="ew")
        self.tree.bind('<Button-1>', self._on_click)
        self.tree.bind('<Configure>', self._update_scrollbars)
        self.tree.bind('<<TreeviewSelect>>', self._update_scrollbars)
        self.tree.bind('<MouseWheel>', self._update_scrollbars)

        self.btn_col_frame = None
        self.btn_add_col = None
        self.btn_row_frame = None
        self.btn_add_row = None
        self.empty_frame = None
        self.log_callback = log_callback
        self.handler = handler

    def _setup_columns(self):
        min_width = 40
        for idx, col in enumerate(self.model.get_columns()):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=max(60, min_width), anchor='center', minwidth=min_width)

    def _load_rows(self):
        self.tree.delete(*self.tree.get_children())
        for row in self.model.get_rows():
            values = [row[0]]
            for checked in row[1:]:
                values.append("☑" if checked else "☐")
            self.tree.insert("", "end", values=values)

    def add_row(self, values=None):
        if self.handler and hasattr(self.handler, 'handle_add_row'):
            self.handler.handle_add_row(self, values)
        else:
            col_count = len(self.model.get_columns())
            if values is None or len(values) != col_count - 1:
                values = [0 for _ in range(col_count - 1)]
            self.model.add_row(values)
            self._load_rows()

    def _on_click(self, event):
        region = self.tree.identify('region', event.x, event.y)
        if region == 'cell':
            item_id = self.tree.identify_row(event.y)
            col = self.tree.identify_column(event.x)
            if item_id and col:
                col_idx = int(col.replace('#', '')) - 1
                if col_idx > 0:
                    idx = self.tree.index(item_id)
                    row = self.model.rows[idx]
                    row[col_idx] = 0 if row[col_idx] else 1
                    self._load_rows()

    def add_column(self, col_name):
        if self.handler and hasattr(self.handler, 'handle_add_column'):
            self.handler.handle_add_column(self, col_name)
        else:
            self.model.add_column(col_name)
            self.tree["columns"] = self.model.get_columns()
            self._setup_columns()
            self._load_rows()

    def hide_treeview(self):
        self.tree.grid_remove()
        self.scrollbar_y.grid_remove()
        self.scrollbar_x.grid_remove()

    def show_treeview(self):
        self.tree.grid()
        self.scrollbar_y.grid()
        self.scrollbar_x.grid()
        if not self.btn_col_frame:
            self.btn_col_frame = tk.Frame(self, bg="#f0f0f0", width=60)
            self.btn_col_frame.grid(row=0, column=1, sticky="ns")
            self.btn_col_frame.grid_propagate(False)
            self.btn_add_col = tk.Button(
                self.btn_col_frame, text="+", font=("Arial", 16), bg="#e6e6e6", borderwidth=0, relief="flat", activebackground="#cccccc",
                command=self.add_column_event
            )
            self.btn_add_col.pack(fill=tk.BOTH, expand=True, padx=8, pady=20)
        if not self.btn_row_frame:
            self.btn_row_frame = tk.Frame(self, bg="#f0f0f0", height=40)
            self.btn_row_frame.grid(row=1, column=0, sticky="ew")
            self.btn_row_frame.grid_propagate(False)
            self.btn_add_row = tk.Button(
                self.btn_row_frame, text="+", font=("Arial", 16), bg="#e6e6e6", borderwidth=0, relief="flat", activebackground="#cccccc",
                command=self.add_row_event
            )
            self.btn_add_row.pack(fill=tk.BOTH, expand=True, padx=20, pady=8)
        if not self.empty_frame:
            self.empty_frame = tk.Frame(self, bg="#f0f0f0", width=60, height=40)
            self.empty_frame.grid(row=1, column=1, sticky="nsew")

    def _update_scrollbars(self, event=None):
        needs_v = len(self.tree.get_children()) > int(self.tree['height'])
        if needs_v:
            self.scrollbar_y.grid()
        else:
            self.scrollbar_y.grid_remove()
        total_width = sum([self.tree.column(col, 'width') for col in self.tree['columns']])
        visible_width = self.tree.winfo_width()
        needs_h = total_width > visible_width
        if needs_h:
            self.scrollbar_x.grid(row=3, column=0, columnspan=3, sticky="ew")
        else:
            self.scrollbar_x.grid_remove()

    def add_row_event(self):
        self.add_row()
        self._update_scrollbars()
        if self.log_callback:
            self.log_callback("행 추가")

    def add_column_event(self):
        new_col_name = f"Col{len(self.model.get_columns())+1}"
        self.add_column(new_col_name)
        self._update_scrollbars()
        if self.log_callback:
            self.log_callback(f"열 추가: {new_col_name}")
