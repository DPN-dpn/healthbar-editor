
import tkinter as tk
from ui.toolbar import Toolbar
from ui.logview import LogView
from ui.matrix_panel import MatrixPanel
from app.handlers import handle_new_project, handle_load_project, handle_edit_project

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

        self.paned = tk.PanedWindow(self.root, orient=tk.VERTICAL)
        self.paned.pack(fill=tk.BOTH, expand=True)

        from app import handlers
        from model.project_model import ProjectModel
        self.project_model = None  # 현재 프로젝트 모델
        self.matrix_panel = MatrixPanel(self.paned, log_callback=self.append_log, handler=handlers)
        self.paned.add(self.matrix_panel, minsize=300, stretch='always')
        self.matrix_panel.hide_treeview()

        self.logview = LogView(self.paned)
        self.paned.add(self.logview, minsize=60)

    def show_treeview_panel(self):
        if self.matrix_panel not in self.paned.panes():
            self.paned.add(self.matrix_panel, stretch='always')

    def handle_load_mode(self):
        self.append_log("모드 불러오기 기능 실행")

    def handle_treeview_width(self):
        self.append_log("트리뷰 폭/너비 설정 기능 실행")

    def append_log(self, msg):
        self.logview.append_log(msg)
