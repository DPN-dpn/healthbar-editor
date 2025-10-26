class TreeViewModel:
    def __init__(self, columns=None):
        self.columns = columns if columns else ["A", "B", "C"]
        self.rows = []

    def add_row(self, values=None):
        if values is None:
            values = ["" for _ in self.columns]
        self.rows.append(values)

    def add_column(self, col_name):
        self.columns.append(col_name)
        for row in self.rows:
            row.append("")

    def get_rows(self):
        return self.rows

    def get_columns(self):
        return self.columns
