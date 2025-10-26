import tkinter as tk

class Toolbar(tk.Frame):
    def __init__(self, master, new_callback, load_callback, edit_callback):
        super().__init__(master, bd=1, relief=tk.RAISED)
        self.pack(side=tk.TOP, fill=tk.X)
        btn_new = tk.Button(self, text="새로 만들기", command=new_callback)
        btn_new.pack(side=tk.LEFT, padx=2, pady=2)
        btn_load = tk.Button(self, text="프로젝트 불러오기", command=load_callback)
        btn_load.pack(side=tk.LEFT, padx=2, pady=2)
        btn_edit = tk.Button(self, text="편집하기", command=edit_callback)
        btn_edit.pack(side=tk.LEFT, padx=2, pady=2)
