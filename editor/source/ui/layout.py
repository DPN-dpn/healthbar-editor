import tkinter as tk
from ui.toolbar import Toolbar
from ui.logview import LogView
from app.handlers import handle_new_project, handle_load_project, handle_edit_project
from ui.treeview import MatrixTreeView

class HealthbarEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Healthbar Editor")
        self.root.geometry("800x600")
        self.toolbar = Toolbar(
            self.root,
            lambda: handle_new_project(self),
            lambda: handle_load_project(self),
            lambda: handle_edit_project(self)
        )

        # 가운데 4분할 레이아웃 프레임
        self.center_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.center_frame.pack(fill=tk.BOTH, expand=True)
        self.center_frame.grid_rowconfigure(0, weight=9)
        self.center_frame.grid_rowconfigure(1, weight=1)
        self.center_frame.grid_columnconfigure(0, weight=1)
        self.center_frame.grid_columnconfigure(1, weight=0)
        # 좌상: Treeview
        from model.treeview_model import TreeViewModel
        self.tree_model = TreeViewModel()
        self.tree = MatrixTreeView(self.center_frame, self.tree_model)
        self.tree.grid(row=0, column=0, sticky="nsew")

        # 우상: 열 추가 +버튼 (너비 고정)
        self.btn_col_frame = tk.Frame(self.center_frame, bg="#f0f0f0", width=60)
        self.btn_col_frame.grid(row=0, column=1, sticky="ns")
        self.btn_col_frame.grid_propagate(False)
        self.btn_add_col = tk.Button(
            self.btn_col_frame, text="+", font=("Arial", 16), bg="#e6e6e6", borderwidth=0, relief="flat", activebackground="#cccccc",
            command=self.add_column_event
        )
        self.btn_add_col.pack(fill=tk.BOTH, expand=True, padx=8, pady=20)

        # 좌하: 행 추가 +버튼
        self.btn_row_frame = tk.Frame(self.center_frame, bg="#f0f0f0", height=40)
        self.btn_row_frame.grid(row=1, column=0, sticky="ew")
        self.btn_row_frame.grid_propagate(False)
        self.btn_add_row = tk.Button(
            self.btn_row_frame, text="+", font=("Arial", 16), bg="#e6e6e6", borderwidth=0, relief="flat", activebackground="#cccccc",
            command=self.add_row_event
        )
        self.btn_add_row.pack(fill=tk.BOTH, expand=True, padx=20, pady=8)

        # 우하: 빈공간
        self.empty_frame = tk.Frame(self.center_frame, bg="#f0f0f0")
        self.empty_frame.grid(row=1, column=1, sticky="nsew")

        self.logview = LogView(self.root)

    def append_log(self, msg):
        self.logview.append_log(msg)

    def add_row_event(self):
        self.tree.add_row()

    def add_column_event(self):
        new_col_name = f"Col{len(self.tree._columns)+1}"
        self.tree.add_column(new_col_name)
