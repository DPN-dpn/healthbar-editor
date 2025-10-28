import tkinter as tk

class Toolbar:
    def __init__(self, master, new_callback, load_callback, mode_callback, treeview_width_callback):
        self.menubar = tk.Menu(master)
        # 파일 메뉴
        file_menu = tk.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="새로 만들기", command=new_callback)
        file_menu.add_separator()
        file_menu.add_command(label="프로젝트 열기", command=load_callback)
        file_menu.add_command(label="프로젝트 저장", command=None)
        file_menu.add_command(label="프로젝트 다른이름으로 저장", command=None)
        file_menu.add_separator()
        file_menu.add_command(label="모드 불러오기", command=mode_callback)
        file_menu.add_command(label="모드 내보내기", command=None)
        self.menubar.add_cascade(label="파일", menu=file_menu)

        # 편집 메뉴
        edit_menu = tk.Menu(self.menubar, tearoff=0)
        edit_menu.add_command(label="실행취소", command=None, state="disabled")
        edit_menu.add_command(label="다시실행", command=None, state="disabled")
        self.menubar.add_cascade(label="편집", menu=edit_menu)

        # 트리뷰 메뉴
        treeview_menu = tk.Menu(self.menubar, tearoff=0)
        treeview_menu.add_command(label="폭/너비 설정", command=treeview_width_callback, state="disabled")
        self.menubar.add_cascade(label="트리뷰", menu=treeview_menu)

        master.config(menu=self.menubar)
        self.file_menu = file_menu
        self.treeview_menu = treeview_menu
