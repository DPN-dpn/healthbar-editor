import tkinter as tk
from ui.toolbar import Toolbar
from ui.logview import LogView
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
            lambda: handle_edit_project(self)
        )
        self.logview = LogView(self.root)

    def append_log(self, msg):
        self.logview.append_log(msg)
