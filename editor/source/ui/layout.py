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
            lambda: self.handle_load_mode(),
            lambda: self.handle_treeview_width()
        )

        # PanedWindow로 CenterMatrixPanel과 LogView를 수직 분할
        self.paned = tk.PanedWindow(self.root, orient=tk.VERTICAL)
        self.paned.pack(fill=tk.BOTH, expand=True)

        self.center_panel = CenterMatrixPanel(self.paned, log_callback=self.append_log)
        self.paned.add(self.center_panel, minsize=300, stretch='always')
        self.center_panel.hide_treeview()  # 처음에는 트리뷰만 숨김

        self.logview = LogView(self.paned)
        self.paned.add(self.logview, minsize=60)

    def show_treeview_panel(self):
        # 트리뷰 패널을 PanedWindow에 추가하여 보이게 함
        if self.center_panel not in self.paned.panes():
            self.paned.add(self.center_panel, stretch='always')

    def handle_load_mode(self):
        self.append_log("모드 불러오기 기능 실행")
        # 실제 모드 불러오기 로직 구현

    def handle_treeview_width(self):
        self.append_log("트리뷰 폭/너비 설정 기능 실행")
        # 실제 폭/너비 설정 로직 구현

    def append_log(self, msg):
        self.logview.append_log(msg)

    def add_row_event(self):
        self.tree.add_row()

    def add_column_event(self):
        new_col_name = f"Col{len(self.tree._columns)+1}"
        self.tree.add_column(new_col_name)

    def show_treeview_panel(self):
        # 트리뷰 패널을 PanedWindow에 추가하여 보이게 함
        if self.center_panel not in self.paned.panes():
            self.paned.add(self.center_panel, stretch='always')

    def handle_load_mode(self):
        self.append_log("모드 불러오기 기능 실행")
        # 실제 모드 불러오기 로직 구현

    def handle_treeview_width(self):
        self.append_log("트리뷰 폭/너비 설정 기능 실행")
        # 실제 폭/너비 설정 로직 구현

    def append_log(self, msg):
        self.logview.append_log(msg)

    def add_row_event(self):
        self.tree.add_row()

    def add_column_event(self):
        new_col_name = f"Col{len(self.tree._columns)+1}"
        self.tree.add_column(new_col_name)
