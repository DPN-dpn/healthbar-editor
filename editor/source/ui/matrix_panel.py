import tkinter as tk
import tkinter.ttk as ttk
from model.treeview_model import TreeViewModel

class MatrixPanel(tk.Frame):
    def set_project_model(self, project_model):
        self.project_model = project_model
        """
        프로젝트 모델을 받아 트리뷰를 동기화
        - 열: hp_step 개수만큼 (Col1, Col2, ...)
        - 행: draw_list 개수만큼, 제목은 draw_list 값
        - 체크박스: checked_list의 값으로 표시
        """
        # 열 정보
        col_count = project_model.hp_step
        columns = [f"Col{i+1}" for i in range(col_count)]
        self.model.columns = columns

        # 행 정보
        self.model.rows = []
        for i, title in enumerate(project_model.draw_list):
            checked_row = project_model.checked_list[i] if i < len(project_model.checked_list) else [False]*col_count
            # 첫 번째 값은 제목, 나머지는 체크 상태
            row = [title] + checked_row
            self.model.rows.append(row)

        self.tree["columns"] = columns
        self._setup_columns()
        self._load_rows()
    def __init__(self, master, log_callback=None, handler=None):
        super().__init__(master, bg="#f0f0f0")
        self.config(width=400, height=300)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)

        self.model = TreeViewModel()
        self.tree = ttk.Treeview(self, columns=self.model.get_columns(), show='headings', selectmode='none', height=15)
        self._setup_columns()
        self._load_rows()
        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.scrollbar_y.grid(row=0, column=2, sticky="ns")
        self.vpad_frame = tk.Frame(self, bg="#f0f0f0", width=8)
        self.vpad_frame.grid(row=0, column=3, sticky="ns")
        self.scrollbar_x.grid(row=2, column=0, columnspan=3, sticky="ew")
        self.tree.bind('<Button-1>', self._on_click)
        self.tree.bind('<Configure>', self._update_scrollbars)
        self.tree.bind('<<TreeviewSelect>>', self._update_scrollbars)
        self.tree.bind('<MouseWheel>', self._update_scrollbars)

        self.log_callback = log_callback
        self.handler = handler

    def _setup_columns(self):
        min_width = 40
        for idx, col in enumerate(self.model.get_columns()):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=max(60, min_width), anchor='center', minwidth=min_width)

    def _load_rows(self):
        self.tree.delete(*self.tree.get_children())
        for row in self.model.get_rows():
            values = [row[0]]
            for checked in row[1:]:
                values.append("☑" if checked else "☐")
            self.tree.insert("", "end", values=values)

    def add_row(self, values=None):
        if self.handler and hasattr(self.handler, 'handle_add_row'):
            self.handler.handle_add_row(self, values)
        else:
            col_count = len(self.model.get_columns())
            if values is None or len(values) != col_count - 1:
                values = [0 for _ in range(col_count - 1)]
            self.model.add_row(values)
            self._load_rows()

    def _on_click(self, event):
        region = self.tree.identify('region', event.x, event.y)
        if region == 'cell':
            item_id = self.tree.identify_row(event.y)
            col = self.tree.identify_column(event.x)
            if item_id and col:
                col_idx = int(col.replace('#', '')) - 1
                if col_idx > 0:
                    idx = self.tree.index(item_id)
                    row = self.model.rows[idx]
                    # 트리뷰 내부 데이터 변경
                    row[col_idx] = 0 if row[col_idx] else 1
                    self._load_rows()
                    # ProjectModel에 반영
                    if hasattr(self, 'project_model') and self.project_model:
                        # checked_list가 없으면 생성
                        while len(self.project_model.checked_list) <= idx:
                            self.project_model.checked_list.append([False]*len(self.model.columns))
                        self.project_model.checked_list[idx][col_idx-1] = bool(row[col_idx])

    def add_column(self, col_name):
        if self.handler and hasattr(self.handler, 'handle_add_column'):
            self.handler.handle_add_column(self, col_name)
        else:
            self.model.add_column(col_name)
            self.tree["columns"] = self.model.get_columns()
            self._setup_columns()
            self._load_rows()

    def hide_treeview(self):
        self.tree.grid_remove()
        self.scrollbar_y.grid_remove()
        self.scrollbar_x.grid_remove()

    def show_treeview(self):
        self.tree.grid()
        self.scrollbar_y.grid()
        self.scrollbar_x.grid()

    def _update_scrollbars(self, event=None):
        needs_v = len(self.tree.get_children()) > int(self.tree['height'])
        if needs_v:
            self.scrollbar_y.grid()
        else:
            self.scrollbar_y.grid_remove()
        total_width = sum([self.tree.column(col, 'width') for col in self.tree['columns']])
        visible_width = self.tree.winfo_width()
        needs_h = total_width > visible_width
        if needs_h:
            self.scrollbar_x.grid(row=3, column=0, columnspan=3, sticky="ew")
        else:
            self.scrollbar_x.grid_remove()

    def add_row_event(self):
        self.add_row()
        self._update_scrollbars()
        if self.log_callback:
            self.log_callback("행 추가")

    def add_column_event(self):
        new_col_name = f"Col{len(self.model.get_columns())+1}"
        self.add_column(new_col_name)
        self._update_scrollbars()
        if self.log_callback:
            self.log_callback(f"열 추가: {new_col_name}")
