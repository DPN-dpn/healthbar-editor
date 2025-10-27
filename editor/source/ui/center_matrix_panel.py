import tkinter as tk
from tkinter import ttk
from model.treeview_model import TreeViewModel
import base64

class MatrixTreeView(ttk.Treeview):
    # 체크박스 이미지 base64 (16x16)
    CHECKED_IMG = (
        'R0lGODlhEAAQAPIAAP///wAAAMLCwgAAAGZmZjMzM////wAAAAAAAAAAACH5BAAAAAAALAAAAAAQABAAAAM6CLrc/jDKSau9OOvNu/9gKI5kaZ5oqubYFADs='
    )
    UNCHECKED_IMG = (
        'R0lGODlhEAAQAPIAAP///wAAAMLCwgAAAGZmZjMzM////wAAAAAAAAAAACH5BAAAAAAALAAAAAAQABAAAAM5CLrc/jDKSau9OOvNu/9gKI5kaZ5oqubYFADs='
    )

    def _load_images(self):
        self.img_checked = tk.PhotoImage(data=base64.b64decode(self.CHECKED_IMG))
        self.img_unchecked = tk.PhotoImage(data=base64.b64decode(self.UNCHECKED_IMG))

    def __init__(self, master, model: TreeViewModel, **kwargs):
        self.model = model
        self._load_images()
        super().__init__(master, columns=self.model.get_columns(), show='headings', selectmode='none', height=15, **kwargs)
        self._setup_columns()
        self._load_rows()
        # 스크롤바 추가
        self.scrollbar_y = ttk.Scrollbar(master, orient="vertical", command=self.yview)
        self.configure(yscrollcommand=self.scrollbar_y.set)
        self.scrollbar_y.grid(row=0, column=2, sticky="ns")
        # 클릭 이벤트 바인딩
        self.bind('<Button-1>', self._on_click)

    def _setup_columns(self):
        for idx, col in enumerate(self.model.get_columns()):
            self.heading(col, text=col)
            # 첫 번째 컬럼(체크박스)은 좁게
            if idx == 0:
                self.column(col, width=30, anchor='center')
            else:
                self.column(col, width=60, anchor='center')

    def _load_rows(self):
        self.delete(*self.get_children())
        for row in self.model.get_rows():
            # 첫 번째 값은 행 제목, 나머지는 체크 상태
            values = [row[0]]
            for checked in row[1:]:
                values.append("☑" if checked else "☐")
            self.insert("", "end", values=values)

    def add_row(self, values=None):
        col_count = len(self.model.get_columns())
        # 나머지 컬럼은 모두 0(미체크)로 초기화
        if values is None or len(values) != col_count - 1:
            values = [0 for _ in range(col_count - 1)]
        self.model.add_row(values)
        self._load_rows()
    def _on_click(self, event):
        # 클릭 위치에서 아이템/컬럼 확인
        region = self.identify('region', event.x, event.y)
        if region == 'cell':
            item_id = self.identify_row(event.y)
            col = self.identify_column(event.x)
            if item_id and col:
                col_idx = int(col.replace('#', '')) - 1
                # 첫 번째 컬럼(행 제목)은 토글 없음, 나머지 컬럼만 토글
                if col_idx > 0:
                    idx = self.index(item_id)
                    row = self.model.rows[idx]
                    # 토글
                    row[col_idx] = 0 if row[col_idx] else 1
                    self._load_rows()

    def add_column(self, col_name):
        self.model.add_column(col_name)
        self["columns"] = self.model.get_columns()
        self._setup_columns()  # 헤더/컬럼 UI 강제 갱신
        self._load_rows()  # 열 추가 후 전체 행 다시 로드

class CenterMatrixPanel(tk.Frame):
    def __init__(self, master, log_callback=None):
        super().__init__(master, bg="#f0f0f0")
        # 레이아웃: 하단(행추가)과 우측(열추가) 고정, 좌상단(트리뷰) 확장
        self.grid_rowconfigure(0, weight=1)   # 트리뷰(확장)
        self.grid_rowconfigure(1, weight=0)   # 행추가버튼(고정)
        self.grid_columnconfigure(0, weight=1) # 트리뷰/행추가버튼(확장)
        self.grid_columnconfigure(1, weight=0) # 열추가버튼(고정)

        # 트리뷰(좌상단, 확장)
        self.tree_model = TreeViewModel()
        self.tree = MatrixTreeView(self, self.tree_model)
        self.tree.grid(row=0, column=0, sticky="nsew")

        # 열 추가 버튼(우측, 고정)
        self.btn_col_frame = tk.Frame(self, bg="#f0f0f0", width=60)
        self.btn_col_frame.grid(row=0, column=1, sticky="ns")
        self.btn_col_frame.grid_propagate(False)
        self.btn_add_col = tk.Button(
            self.btn_col_frame, text="+", font=("Arial", 16), bg="#e6e6e6", borderwidth=0, relief="flat", activebackground="#cccccc",
            command=self.add_column_event
        )
        self.btn_add_col.pack(fill=tk.BOTH, expand=True, padx=8, pady=20)

        # 행 추가 버튼(하단, 고정)
        self.btn_row_frame = tk.Frame(self, bg="#f0f0f0", height=40)
        self.btn_row_frame.grid(row=1, column=0, sticky="ew")
        self.btn_row_frame.grid_propagate(False)
        self.btn_add_row = tk.Button(
            self.btn_row_frame, text="+", font=("Arial", 16), bg="#e6e6e6", borderwidth=0, relief="flat", activebackground="#cccccc",
            command=self.add_row_event
        )
        self.btn_add_row.pack(fill=tk.BOTH, expand=True, padx=20, pady=8)

        # 빈공간(우하, 최소)
        self.empty_frame = tk.Frame(self, bg="#f0f0f0", width=60, height=40)
        self.empty_frame.grid(row=1, column=1, sticky="nsew")

        self.log_callback = log_callback

    def add_row_event(self):
        self.tree.add_row()
        if self.log_callback:
            self.log_callback("행 추가")

    def add_column_event(self):
        new_col_name = f"Col{len(self.tree_model.get_columns())+1}"
        self.tree.add_column(new_col_name)
        if self.log_callback:
            self.log_callback(f"열 추가: {new_col_name}")
