import tkinter as tk

class Toolbar:
    def __init__(self, master, new_callback, load_callback, mode_callback, treeview_width_callback):
        self.menubar = tk.Menu(master)
        # 파일 메뉴
        file_menu = tk.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="새로 만들기", command=new_callback)
        file_menu.add_command(label="프로젝트 열기", command=load_callback)
        file_menu.add_command(label="모드 불러오기", command=mode_callback)
        self.menubar.add_cascade(label="파일", menu=file_menu)

        # 트리뷰 메뉴
        treeview_menu = tk.Menu(self.menubar, tearoff=0)
        treeview_menu.add_command(label="폭/너비 설정", command=treeview_width_callback)
        self.menubar.add_cascade(label="트리뷰", menu=treeview_menu)

        master.config(menu=self.menubar)
