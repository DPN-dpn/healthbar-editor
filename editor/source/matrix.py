import tkinter as tk


class MatrixUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master, background="#f0f0f0")
        self.pack_propagate(False)
        self.canvas = tk.Canvas(self, borderwidth=0, background="#f0f0f0")
        self.scroll_y = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scroll_x = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=(10,0))
        self.frame = tk.Frame(self.canvas, background="#f0f0f0")
        self.canvas.create_window((0,0), window=self.frame, anchor="nw")
        self.frame.bind("<Configure>", self.on_frame_configure)

        self.row_titles = []
        self.col_titles = []
        self.checkbox_vars = []

        self.create_matrix()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def create_matrix(self):
        # 전체 UI 초기화
        for widget in self.frame.winfo_children():
            widget.destroy()

        # 레이아웃 개편: 1x1 행렬(제목행/열 포함) + 버튼 분리
        common_font = ("Arial", 11)
        common_bg = "#e6e6e6"
        common_bd = 0
        common_relief = "flat"

        # 최소 1행 1열 보장
        if not self.row_titles:
            self.row_titles.append("행1")
        if not self.col_titles:
            self.col_titles.append("열1")
        if not self.checkbox_vars or len(self.checkbox_vars) != len(self.row_titles):
            self.checkbox_vars = []
            for _ in self.row_titles:
                self.checkbox_vars.append([tk.IntVar() for _ in self.col_titles])
        else:
            for row_vars in self.checkbox_vars:
                while len(row_vars) < len(self.col_titles):
                    row_vars.append(tk.IntVar())

        # 제목행
        tk.Label(self.frame, text="", width=8, bg=common_bg, borderwidth=common_bd, relief=common_relief).grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        for col, title in enumerate(self.col_titles):
            # 열 제목 라벨 + 삭제 버튼을 한 줄에 Frame으로 묶음
            col_title_frame = tk.Frame(self.frame, bg=common_bg)
            col_title_frame.grid(row=0, column=col+1, padx=0, pady=0, sticky="nsew")
            tk.Label(col_title_frame, text=title, font=common_font, width=8, height=2, bg=common_bg, borderwidth=common_bd, relief=common_relief).pack(side=tk.LEFT, fill="y")
            btn_del_col = tk.Button(col_title_frame, text="-", command=lambda c=col: self.delete_column(c), font=common_font, bg=common_bg, borderwidth=common_bd, relief=common_relief, activebackground="#cccccc")
            btn_del_col.pack(side=tk.LEFT, fill="y")
        # 제목열 및 체크박스
        for row, title in enumerate(self.row_titles):
            # 행 제목 라벨 + 삭제 버튼을 한 줄에 Frame으로 묶음
            row_title_frame = tk.Frame(self.frame, bg=common_bg)
            row_title_frame.grid(row=row+1, column=0, padx=0, pady=0, sticky="nsew")
            tk.Label(row_title_frame, text=title, font=common_font, width=8, height=2, bg=common_bg, borderwidth=common_bd, relief=common_relief).pack(side=tk.LEFT, fill="x")
            btn_del_row = tk.Button(row_title_frame, text="-", command=lambda r=row: self.delete_row(r), font=common_font, bg=common_bg, borderwidth=common_bd, relief=common_relief, activebackground="#cccccc")
            btn_del_row.pack(side=tk.LEFT, fill="x")
            for col in range(len(self.col_titles)):
                chk = tk.Checkbutton(self.frame, variable=self.checkbox_vars[row][col], width=4, height=2, font=common_font, bg=common_bg, bd=0, highlightthickness=0, relief=common_relief, activebackground="#cccccc")
                chk.grid(row=row+1, column=col+1, padx=0, pady=0, sticky="nsew")

        # 열 추가 버튼: 행렬 오른쪽에 세로로 길게
        btn_add_col = tk.Button(self.frame, text="+", command=self.add_column, font=common_font, bg=common_bg, borderwidth=common_bd, relief=common_relief, activebackground="#cccccc")
        btn_add_col.grid(row=0, column=len(self.col_titles)+1, rowspan=len(self.row_titles)+1, padx=(10,0), pady=0, sticky="ns")
        self.frame.grid_columnconfigure(len(self.col_titles)+1, weight=0)

        # 행 추가 버튼: 행렬 하단에 가로로 길게
        btn_add_row = tk.Button(self.frame, text="+", command=self.add_row, font=common_font, bg=common_bg, borderwidth=common_bd, relief=common_relief, activebackground="#cccccc")
        btn_add_row.grid(row=len(self.row_titles)+1, column=0, columnspan=len(self.col_titles)+1, padx=0, pady=(10,0), sticky="ew")
        self.frame.grid_rowconfigure(len(self.row_titles)+1, weight=0)
        for c in range(len(self.col_titles)+1):
            self.frame.grid_columnconfigure(c, weight=1)

    def add_column(self):
        # 새 열 제목 추가
        new_col_idx = len(self.col_titles) + 1
        self.col_titles.append(f"열{new_col_idx}")
        # 각 행에 체크박스 변수 추가
        for row_vars in self.checkbox_vars:
            row_vars.append(tk.IntVar())
        self.create_matrix()

    def add_row(self):
        # 새 행 제목 추가
        new_row_idx = len(self.row_titles) + 1
        self.row_titles.append(f"행{new_row_idx}")
        # 새 행의 체크박스 변수 리스트 생성
        new_row_vars = [tk.IntVar() for _ in range(len(self.col_titles))]
        self.checkbox_vars.append(new_row_vars)
        self.create_matrix()

