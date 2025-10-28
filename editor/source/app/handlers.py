# 기능 핸들러 모듈

def handle_new_project(app):
    from model.project_model import ProjectModel
    app.project_model = ProjectModel()
    app.matrix_panel.set_project_model(app.project_model)
    app.append_log("새 프로젝트 생성 기능 실행")
    app.matrix_panel.show_treeview()
    # 실제 새 프로젝트 생성 로직 구현

def handle_load_project(app):
    app.append_log("프로젝트 불러오기 기능 실행")
    # 실제 프로젝트 불러오기 로직 구현

def handle_edit_project(app):
    app.append_log("편집 기능 실행")
    # 실제 편집 로직 구현

def handle_add_row(panel, values=None):
    col_count = len(panel.model.get_columns())
    if values is None or len(values) != col_count - 1:
        values = [0 for _ in range(col_count - 1)]
    panel.model.add_row(values)
    panel._load_rows()

def handle_add_column(panel, col_name):
    panel.model.add_column(col_name)
    panel.tree["columns"] = panel.model.get_columns()
    panel._setup_columns()
    panel._load_rows()
