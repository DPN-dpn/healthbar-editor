class TreeViewModel:
    def __init__(self, columns=None):
        # 첫 번째 컬럼을 'No'(행 번호)로 고정
        base_columns = columns if columns else ["A", "B", "C"]
        self.columns = ["No"] + base_columns
        self.rows = []

    def add_row(self, values=None):
        # 첫 번째 값은 임시 행 제목("행N")
        row_title = f"행{len(self.rows) + 1}"
        col_count = len(self.columns)
        # 나머지 컬럼은 모두 0(미체크)로 초기화
        if values is None or len(values) != col_count - 1:
            values = [0 for _ in range(col_count - 1)]
        full_values = [row_title] + values
        self.rows.append(full_values)

    def add_column(self, col_name):
        self.columns.append(col_name)
        for row in self.rows:
            row.append("")

    def get_rows(self):
        return self.rows

    def get_columns(self):
        return self.columns
