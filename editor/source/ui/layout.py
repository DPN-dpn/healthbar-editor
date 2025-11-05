import tkinter as tk
import tkinter.ttk as ttk
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

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # 첫 번째 탭(설정)
        self.empty_tab = tk.Frame(self.notebook)
        self.notebook.add(self.empty_tab, text="설정")
        self.load_mode_btn = tk.Button(self.empty_tab, text="모드불러오기", command=self.handle_load_mode)
        self.load_mode_btn.pack(pady=20)

        # 두 번째 탭(트리뷰)
        from model.project_model import ProjectModel
        self.project_model = None  # 현재 프로젝트 모델
        self.matrix_panel = MatrixPanel(self.notebook, log_callback=self.append_log, handler=handle_new_project)
        # 최초에는 트리뷰 탭을 추가하지 않음

        # 로그뷰는 하단에 별도로 배치
        self.logview = LogView(self.root)
        self.logview.pack(fill=tk.X, side=tk.BOTTOM)

    def show_treeview_panel(self):
        # 프로젝트가 열릴 때 트리뷰 탭 추가
        if self.matrix_panel not in self.notebook.tabs():
            self.notebook.add(self.matrix_panel, text="트리뷰")

    def hide_treeview_panel(self):
        # 프로젝트가 없으면 트리뷰 탭 제거
        if self.matrix_panel in self.notebook.tabs():
            self.notebook.forget(self.matrix_panel)

    def handle_load_mode(self):
        self.append_log("모드 불러오기 기능 실행")

    def handle_treeview_width(self):
        self.append_log("트리뷰 폭/너비 설정 기능 실행")

    def append_log(self, msg):
        self.logview.append_log(msg)
