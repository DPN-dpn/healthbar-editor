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
        self.create_matrix()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_matrix(self):
        top_label = tk.Label(self.frame, text="행렬 체크박스 UI", font=("Arial", 12, "bold"))
        top_label.grid(row=0, column=0, columnspan=5, pady=(0,10))
        for col in range(1, 5):
            step_label = tk.Label(self.frame, text=str(col), font=("Arial", 10, "bold"))
            step_label.grid(row=1, column=col, padx=5, pady=5)
        row_titles = ["A단계", "B단계", "C단계", "D단계", "E단계"]
        for row in range(2, 7):
            title_label = tk.Label(self.frame, text=row_titles[row-2], font=("Arial", 10, "bold"))
            title_label.grid(row=row, column=0, padx=5, pady=5)
        self.checkbox_vars = []
        for i in range(5):
            row_vars = []
            for j in range(4):
                var = tk.IntVar()
                cell_frame = tk.Frame(self.frame, width=80, height=40, bg="#f0f0f0", highlightbackground="#cccccc", highlightthickness=1)
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
