import tkinter as tk
from tkinter import ttk
from model.treeview_model import TreeViewModel
import base64

class MatrixTreeView(ttk.Treeview):
    def __init__(self, master, model: TreeViewModel, **kwargs):
        self.model = model
        super().__init__(master, columns=self.model.get_columns(), show='headings', selectmode='none', height=15, **kwargs)
        self._setup_columns()
        self._load_rows()
        # 스크롤바 추가 (self가 Frame이 아니라 Treeview이므로, grid는 부모에서 해야 함)
        self.scrollbar_y = ttk.Scrollbar(master, orient="vertical", command=self.yview)
        self.scrollbar_x = ttk.Scrollbar(master, orient="horizontal", command=self.xview)
        self.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
        # 클릭 이벤트 바인딩
        self.bind('<Button-1>', self._on_click)

    def _setup_columns(self):
        min_width = 40
        for idx, col in enumerate(self.model.get_columns()):
            self.heading(col, text=col)
            # 첫 번째 컬럼(행 제목)은 좁게
            if idx == 0:
                self.column(col, width=max(60, min_width), anchor='center', minwidth=min_width)
            else:
                self.column(col, width=max(60, min_width), anchor='center', minwidth=min_width)

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
        # 레이아웃: 트리뷰(0,0), 열추가버튼(0,1), 세로스크롤(0,2), 패딩(0,3), 행추가버튼(1,0), 가로스크롤(2,0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)

        # 트리뷰
        self.tree_model = TreeViewModel()
        self.tree = MatrixTreeView(self, self.tree_model)
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.scrollbar_y.grid(row=0, column=2, sticky="ns")
        self.vpad_frame = tk.Frame(self, bg="#f0f0f0", width=8)
        self.vpad_frame.grid(row=0, column=3, sticky="ns")
        self.tree.scrollbar_x.grid(row=2, column=0, columnspan=3, sticky="ew")
        self.tree.bind('<Configure>', self._update_scrollbars)
        self.tree.bind('<<TreeviewSelect>>', self._update_scrollbars)
        self.tree.bind('<MouseWheel>', self._update_scrollbars)

        # 열 추가 버튼
        self.btn_col_frame = tk.Frame(self, bg="#f0f0f0", width=60)
        self.btn_col_frame.grid(row=0, column=1, sticky="ns")
        self.btn_col_frame.grid_propagate(False)
        self.btn_add_col = tk.Button(
            self.btn_col_frame, text="+", font=("Arial", 16), bg="#e6e6e6", borderwidth=0, relief="flat", activebackground="#cccccc",
            command=self.add_column_event
        )
        self.btn_add_col.pack(fill=tk.BOTH, expand=True, padx=8, pady=20)

        # 행 추가 버튼
        self.btn_row_frame = tk.Frame(self, bg="#f0f0f0", height=40)
        self.btn_row_frame.grid(row=1, column=0, sticky="ew")
        self.btn_row_frame.grid_propagate(False)
        self.btn_add_row = tk.Button(
            self.btn_row_frame, text="+", font=("Arial", 16), bg="#e6e6e6", borderwidth=0, relief="flat", activebackground="#cccccc",
            command=self.add_row_event
        )
        self.btn_add_row.pack(fill=tk.BOTH, expand=True, padx=20, pady=8)

        # 빈공간(우하)
        self.empty_frame = tk.Frame(self, bg="#f0f0f0", width=60, height=40)
        self.empty_frame.grid(row=1, column=1, sticky="nsew")

        # log_callback 인스턴스 변수 등록
        self.log_callback = log_callback

    def _update_scrollbars(self, event=None):
        # 세로 스크롤 필요 여부 판단
        needs_v = len(self.tree.get_children()) > int(self.tree['height'])
        if needs_v:
            self.tree.scrollbar_y.grid()
        else:
            self.tree.scrollbar_y.grid_remove()
        # 가로 스크롤 필요 여부 판단
        total_width = sum([self.tree.column(col, 'width') for col in self.tree['columns']])
        visible_width = self.tree.winfo_width()
        needs_h = total_width > visible_width
        if needs_h:
            self.tree.scrollbar_x.grid(row=3, column=0, columnspan=3, sticky="ew")
        else:
            self.tree.scrollbar_x.grid_remove()

    def add_row_event(self):
        self.tree.add_row()
        self._update_scrollbars()  # 행 추가 후 스크롤바 갱신
        if self.log_callback:
            self.log_callback("행 추가")

    def add_column_event(self):
        new_col_name = f"Col{len(self.tree_model.get_columns())+1}"
        self.tree.add_column(new_col_name)
        self._update_scrollbars()  # 열 추가 후 스크롤바 갱신
        if self.log_callback:
            self.log_callback(f"열 추가: {new_col_name}")
