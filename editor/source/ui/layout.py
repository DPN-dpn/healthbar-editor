import tkinter as tk
from ui.toolbar import Toolbar
from ui.logview import LogView
from app.handlers import handle_new_project, handle_load_project, handle_edit_project
from ui.center_matrix_panel import CenterMatrixPanel

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

        # 가운데 4분할 UI를 CenterMatrixPanel로 대체
        self.center_panel = CenterMatrixPanel(self.root, log_callback=self.append_log)
        self.center_panel.pack(fill=tk.BOTH, expand=True)

        self.logview = LogView(self.root)

    def append_log(self, msg):
        self.logview.append_log(msg)

    def add_row_event(self):
        self.tree.add_row()

    def add_column_event(self):
        new_col_name = f"Col{len(self.tree._columns)+1}"
        self.tree.add_column(new_col_name)
