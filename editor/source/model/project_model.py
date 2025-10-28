class ProjectModel:
    """
    프로젝트 정보를 저장하는 모델 클래스
    - name: 프로젝트명
    - hp_step: 체력 단계 (기본값 1)
    - draw_list: draw 리스트 (기본값 빈 리스트)
    - checked_list: 체크목록 (기본값 빈 리스트)
    """
    def __init__(self, name=None, hp_step=1, draw_list=None, checked_list=None):
        self.name = name if name is not None else "새 프로젝트"
        self.hp_step = hp_step
        self.draw_list = draw_list if draw_list is not None else []
        self.checked_list = checked_list if checked_list is not None else []
