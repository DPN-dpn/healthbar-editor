import os
import re
import sys

def is_valid_agent_name(name: str) -> bool:
    if not name:
        print("[오류] 에이전트 이름이 비어있습니다.")
        return False
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name):
        print("[오류] 에이전트 이름은 영문, 숫자, 언더스코어만 사용 가능하며, 첫 글자는 영문 또는 언더스코어여야 합니다.")
        return False
    if re.search(r'[ㄱ-ㅎㅏ-ㅣ가-힣]', name):
        print("[오류] 한글은 사용할 수 없습니다.")
        return False
    if ' ' in name:
        print("[오류] 공백은 사용할 수 없습니다.")
        return False
    return True

def ask_agent_info():
    while True:
        agent_name = input("에이전트 이름을 입력하세요: ").strip()
        if is_valid_agent_name(agent_name):
            break
        else:
            print("다시 입력해 주세요.\n")
    print("Blend 해시값(16진수 8글자, 예: 1a2b3c4d)을 입력하세요.")
    while True:
        h = input("해시값: ").strip()
        if not h:
            print("[오류] 해시값이 비어있습니다. 다시 입력하세요.")
        elif not re.fullmatch(r'[0-9a-fA-F]{8}', h):
            print("[오류] 해시값은 16진수 8글자여야 합니다. 다시 입력하세요.")
        else:
            return agent_name, h

def load_ini(ini_path):
    with open(ini_path, encoding="utf-8") as f:
        return f.read().splitlines()

def agent_exists(lines, name):
    for line in lines:
        if f"CommandList\\Healthbar\\{name}" in line or f"global ${name} = 1" in line or f"global $Is{name} = 0" in line:
            return True
    return False

def hash_exists(lines, hash_value):
    hash_value = hash_value.lower()
    for line in lines:
        if line.strip().startswith("hash ="):
            exist_hash = line.strip().split("=")[1].strip().lower()
            if exist_hash == hash_value:
                return True
    return False

def insert_last_block(ini_path, agent_name, hash_value):
    with open(ini_path, encoding="utf-8") as f:
        lines = f.readlines()

    # 모든 [LAST_START]~[LAST_END] 블록 위치 찾기
    idx = 0
    insert_positions = []  # (start_idx, end_idx) 쌍 리스트
    while idx < len(lines):
        if '[LAST_START]' in lines[idx]:
            start_idx = idx
            # end_idx 찾기
            end_idx = None
            for j in range(start_idx+1, len(lines)):
                if '[LAST_END]' in lines[j]:
                    end_idx = j
                    break
            if end_idx is not None and end_idx > start_idx:
                insert_positions.append((start_idx, end_idx))
                idx = end_idx + 1
            else:
                print(f'[오류] [LAST_START]~[LAST_END] 쌍이 올바르지 않습니다. (index {start_idx})')
                idx += 1
        else:
            idx += 1

    if not insert_positions:
        print('[오류] [LAST_START]~[LAST_END] 블록을 찾을 수 없습니다.')
        return

    # 줄 밀림 방지를 위해 역순으로 처리
    import re
    # [NUM_xx] 키워드 치환 함수
    def replace_num_keyword(s):
        return re.sub(r'\[NUM_(\d+)\]', lambda m: m.group(1), s)

    # 현재 파일에서 가장 큰 [NUM_xx] 값 찾기
    num_pattern = re.compile(r'\[NUM_(\d+)\]')
    max_num = 0
    for line in lines:
        for m in num_pattern.finditer(line):
            n = int(m.group(1))
            if n > max_num:
                max_num = n

    next_num = max_num + 1

    for start_idx, end_idx in reversed(insert_positions):
        block = []
        for line in lines[start_idx+1:end_idx]:
            # 주석 또는 공백줄 모두 복제
            if line.strip() == '':
                block.append(line)
            elif line.lstrip().startswith(';'):
                idx2 = line.find(';')
                if idx2 != -1:
                    new_line = line[:idx2] + line[idx2+1:]
                else:
                    new_line = line
                new_line = new_line.replace('[AGENT]', agent_name).replace('[HASH]', hash_value)
                new_line = replace_num_keyword(new_line)
                block.append(new_line)
        # [LAST_START]보다 한 줄 더 위에 삽입
        insert_at = max(0, start_idx - 1)
        lines = lines[:insert_at] + block + lines[insert_at:]

    # [NUM_xx] 블록의 숫자 1 증가
    for i, line in enumerate(lines):
        if '[NUM_' in line:
            m = num_pattern.search(line)
            if m:
                old_num = int(m.group(1))
                new_num = old_num + 1
                lines[i] = line.replace(f'[NUM_{old_num}]', f'[NUM_{new_num}]')
                break

    with open(ini_path, 'w', encoding='utf-8') as f:
        for line in lines:
            if not line.endswith('\n'):
                f.write(line + '\n')
            else:
                f.write(line)
    print(f'[안내] {agent_name} 블록 복제 및 치환 완료 (총 {len(insert_positions)}곳)')

def main():
    try:
        ini_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Healthbar.ini")
        if not os.path.exists(ini_path):
            print(f"Healthbar.ini 파일이 없습니다: {ini_path}")
            sys.exit(1)
        lines = load_ini(ini_path)
        name = input("에이전트 이름을 입력하세요: ").strip()
        if not is_valid_agent_name(name):
            print("[오류] 에이전트 이름이 올바르지 않습니다.")
            sys.exit(1)
        if agent_exists(lines, name):
            print(f"이미 존재하는 에이전트 이름입니다: {name}")
            yn = input("스킨을 추가하시겠습니까? (y/n): ").strip().lower()
            if yn != 'y':
                print("작업을 종료합니다.")
                sys.exit(0)
            # 스킨 추가 로직
            print("해시값(16진수 8글자, 예: 1a2b3c4d)을 입력하세요.")
            while True:
                hash_value = input("해시값: ").strip()
                if not hash_value:
                    print("[오류] 해시값이 비어있습니다. 다시 입력하세요.")
                elif not re.fullmatch(r'[0-9a-fA-F]{8}', hash_value):
                    print("[오류] 해시값은 16진수 8글자여야 합니다. 다시 입력하세요.")
                elif hash_exists(lines, hash_value):
                    print(f"이미 존재하는 해시값입니다: {hash_value}")
                else:
                    break

            # 블록 탐색: ; MARK: name ~ post $Is{name} = 0 까지
            mark_line = f'; MARK: {name}'
            post_line = f'post $Is{name} = 0'
            start_idx = end_idx = None
            for i, line in enumerate(lines):
                if line.strip() == mark_line:
                    start_idx = i
                if start_idx is not None and line.strip() == post_line:
                    end_idx = i
                    break
            if start_idx is None or end_idx is None:
                print(f"[오류] 해당 에이전트의 블록을 찾을 수 없습니다.")
                sys.exit(1)

            # TextureOverride 블록만 추출 (endif 포함)
            tex_blocks = []
            i = start_idx
            while i <= end_idx:
                if lines[i].strip().startswith('[TextureOverride'):
                    block_start = i
                    block_end = None
                    for j in range(i+1, end_idx+1):
                        if lines[j].strip() == 'endif':
                            block_end = j  # endif 줄까지 포함
                            break
                        elif lines[j].strip().startswith('[') and j != block_start:
                            block_end = j - 1  # 이전 줄까지 포함
                            break
                    if block_end is None:
                        block_end = end_idx
                    tex_blocks.append((block_start, block_end+1))  # block_end+1로 슬라이싱
                    i = block_end + 1
                else:
                    i += 1

            if not tex_blocks:
                print(f"[오류] TextureOverride 블록을 찾을 수 없습니다.")
                sys.exit(1)

            # 복제 및 치환
            new_lines = []
            # 복제된 블록 앞에 빈 줄 추가
            new_lines.append('\n')
            for block_start, block_end in tex_blocks:
                for k in range(block_start, block_end):
                    line = lines[k]
                    # 섹션 헤더 치환
                    if line.strip().startswith('[TextureOverride'):
                        # [TextureOverride Name Body Blend] → [TextureOverride Name Skin Body Blend]
                        new_line = line.replace(f'{name} Body Blend', f'{name} Skin Body Blend')
                    elif 'hash =' in line:
                        new_line = re.sub(r'hash\s*=.*', f'hash = {hash_value}', line)
                    else:
                        new_line = line
                    new_lines.append(new_line)
            # 복제된 블록을 원본 TextureOverride 블록 바로 아래에 삽입
            insert_pos = tex_blocks[-1][1]
            lines = lines[:insert_pos] + new_lines + lines[insert_pos:]

            with open(ini_path, 'w', encoding='utf-8') as f:
                for line in lines:
                    if not line.endswith('\n'):
                        f.write(line + '\n')
                    else:
                        f.write(line)
            print(f'[안내] {name}의 스킨 TextureOverride 블록이 추가되었습니다.')
            sys.exit(0)
        else:
            print("Blend 해시값(16진수 8글자, 예: 1a2b3c4d)을 입력하세요.")
            while True:
                hash_value = input("해시값: ").strip()
                if not hash_value:
                    print("[오류] 해시값이 비어있습니다. 다시 입력하세요.")
                elif not re.fullmatch(r'[0-9a-fA-F]{8}', hash_value):
                    print("[오류] 해시값은 16진수 8글자여야 합니다. 다시 입력하세요.")
                elif hash_exists(lines, hash_value):
                    print(f"이미 존재하는 해시값입니다: {hash_value}")
                else:
                    break
            insert_last_block(ini_path, name, hash_value)
    except KeyboardInterrupt:
        print("\n[안내] 작업이 사용자의 요청(Ctrl+C)으로 취소되었습니다.")
        sys.exit(0)

if __name__ == "__main__":
    main()
