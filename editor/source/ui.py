import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class HealthbarEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Healthbar Editor")
        self.root.geometry("800x600")
        self.create_toolbar()
        self.create_matrix_ui()
        self.create_log_ui()

    def create_toolbar(self):
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        btn_new = tk.Button(toolbar, text="새로 만들기", command=self.new_project)
        btn_new.pack(side=tk.LEFT, padx=2, pady=2)
        btn_load = tk.Button(toolbar, text="프로젝트 불러오기", command=self.load_project)
        btn_load.pack(side=tk.LEFT, padx=2, pady=2)
        btn_edit = tk.Button(toolbar, text="편집하기", command=self.edit_project)
        btn_edit.pack(side=tk.LEFT, padx=2, pady=2)

    def create_matrix_ui(self):
        self.matrix_canvas = tk.Canvas(self.root, borderwidth=0, background="#f0f0f0")
        self.matrix_scroll_y = tk.Scrollbar(self.root, orient="vertical", command=self.matrix_canvas.yview)
        self.matrix_scroll_x = tk.Scrollbar(self.root, orient="horizontal", command=self.matrix_canvas.xview)
        self.matrix_canvas.configure(yscrollcommand=self.matrix_scroll_y.set, xscrollcommand=self.matrix_scroll_x.set)
        self.matrix_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.matrix_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.matrix_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=(10,0))
        self.matrix_frame = tk.Frame(self.matrix_canvas, background="#f0f0f0")
        self.matrix_canvas.create_window((0,0), window=self.matrix_frame, anchor="nw")
        self.matrix_frame.bind("<Configure>", self.on_frame_configure)

        # 병합된 상단 라벨
        top_label = tk.Label(self.matrix_frame, text="행렬 체크박스 UI", font=("Arial", 12, "bold"))
        top_label.grid(row=0, column=0, columnspan=5, pady=(0,10))

        # 제목행 (1~4 단계)
        for col in range(1, 5):
            step_label = tk.Label(self.matrix_frame, text=str(col), font=("Arial", 10, "bold"))
            step_label.grid(row=1, column=col, padx=5, pady=5)

        # 제목열 (2단계)
        row_titles = ["A단계", "B단계", "C단계", "D단계", "E단계"]
        for row in range(2, 7):
            title_label = tk.Label(self.matrix_frame, text=row_titles[row-2], font=("Arial", 10, "bold"))
            title_label.grid(row=row, column=0, padx=5, pady=5)

        # 체크박스 행렬 생성 (5x4) - 칸 넓게, 셀 전체 클릭 가능
        self.checkbox_vars = []
        for i in range(5):
            row_vars = []
            for j in range(4):
                var = tk.IntVar()
                cell_frame = tk.Frame(self.matrix_frame, width=80, height=40, bg="#f0f0f0", highlightbackground="#cccccc", highlightthickness=1)
                cell_frame.grid_propagate(False)
                cell_frame.grid(row=i+2, column=j+1, padx=5, pady=5, sticky="nsew")
                chk = tk.Checkbutton(cell_frame, variable=var, width=6, height=2, bg="#f0f0f0", bd=0, highlightthickness=0)
                chk.pack(expand=True, fill="both")
                def toggle(var=var):
                    var.set(0 if var.get() else 1)
                cell_frame.bind("<Button-1>", lambda e, v=var: toggle(v))
                chk.bind("<Button-1>", lambda e: None)
                row_vars.append(var)
            self.checkbox_vars.append(row_vars)

    def on_frame_configure(self, event):
        self.matrix_canvas.configure(scrollregion=self.matrix_canvas.bbox("all"))

    def create_log_ui(self):
        log_frame = tk.Frame(self.root)
        log_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        self.log_text = ScrolledText(log_frame, height=6, state="disabled", font=("Consolas", 10))
        self.log_text.pack(fill=tk.X)

    def append_log(self, msg):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def new_project(self):
        self.append_log("새로 만들기 클릭")

    def load_project(self):
        self.append_log("프로젝트 불러오기 클릭")

    def edit_project(self):
        self.append_log("편집하기 클릭")
