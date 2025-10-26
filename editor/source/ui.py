
import tkinter as tk
from toolbar import Toolbar
from logview import LogView

class HealthbarEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Healthbar Editor")
        self.root.geometry("800x600")
        self.toolbar = Toolbar(self.root, self.new_project, self.load_project, self.edit_project)
        self.logview = LogView(self.root)

    def append_log(self, msg):
        self.logview.append_log(msg)

    def new_project(self):
        self.append_log("새로 만들기 클릭")

    def load_project(self):
        self.append_log("프로젝트 불러오기 클릭")

    def edit_project(self):
        self.append_log("편집하기 클릭")
