class TreeViewModel:
    def __init__(self, columns=None):
        # 첫 번째 컬럼을 'No'(행 번호)로 고정
        base_columns = columns if columns else ["A", "B", "C"]
        self.columns = ["No"] + base_columns
        self.rows = []

    def add_row(self, values=None):
        # 첫 번째 값은 행 번호로 자동 지정
        row_num = str(len(self.rows) + 1)
        if values is None:
            values = ["" for _ in self.columns[1:]]
        # 첫 번째 값에 행 번호 삽입
        full_values = [row_num] + values
        self.rows.append(full_values)

    def add_column(self, col_name):
        self.columns.append(col_name)
        for row in self.rows:
            row.append("")

    def get_rows(self):
        return self.rows

    def get_columns(self):
        return self.columns
