import random

import numpy as np
import time
from pympler import asizeof
from collections import deque

# tt: trạng thái
# 2: vị trí nhân vật (start)
# 3: vị trí goal

matrix = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 3],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

DICHUYEN = [(0,1),(1,0),(0,-1),(-1,0)]

class BacktrackingAC3:
    def __init__(self, ma_tran=None):
        if ma_tran is None:
            ma_tran = matrix
        self.tt_bandau = np.array(ma_tran)
        self.num_rows, self.num_cols = self.tt_bandau.shape

        # lưu thứ tự các trạng thái đã duyệt
        self.list_tt_duyet = []
        # lưu đường đi
        self.duong_di = []

        # Các thông số để so sánh
        self.So_tt_daduyet = 0  # số trạng thái đã duyệt
        self.So_tt_dasinh = 0  # số trạng thái đã sinh/được xem xét
        self.Kichthuoc_bonho = 0  # Số tt ở thời điểm stack max
        self.Kichthuoc_bonho_MB = 0.0  # kích thước bộ nhớ max
        self.Dodai_duongdi = 0  # chiều dài đường đi
        self.execution_time = 0  # thời gian thực thi

    def tim_vitri(self, gia_tri):
        list_toado = np.argwhere(self.tt_bandau == gia_tri)
        return [tuple(p) for p in list_toado]

    def thong_so(self):
        return {
            "So tt da duyet": self.So_tt_daduyet,
            "So tt da sinh": self.So_tt_dasinh,
            "Kich thuoc bo nho (tt)": self.Kichthuoc_bonho,
            "Kich thuoc bo nho (MB)": round(self.Kichthuoc_bonho_MB, 6),
            "Do dai duong di": self.Dodai_duongdi,
            "Execution time (s)": round(self.execution_time, 6)
        }

    def is_valid_move(self, x, y, visited):
        if 0 <= x < self.num_rows and 0 <= y < self.num_cols:
            if self.tt_bandau[x, y] != 1 and (x, y) not in visited:
                return True
        return False

    # --- AC-3 ---
    def tao_domain(self, da_di):
        domain = {}
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if (r, c) in da_di or self.tt_bandau[r, c] == 1:
                    domain[(r, c)] = {0}
                else:
                    domain[(r, c)] = {0, 1}
        return domain

    def tao_rang_buoc(self):
        queue = deque()
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                for dr, dc in DICHUYEN:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.num_rows and 0 <= nc < self.num_cols:
                        queue.append(((r, c), (nr, nc)))
        return queue

    def revise(self, domain, xi, xj):
        revised = False
        if 1 in domain[xi]:
            if not any(v == 1 for v in domain[xj]):
                domain[xi].remove(1)
                revised = True
        return revised

    def ac3(self, domain):
        queue = self.tao_rang_buoc()
        while queue:
            xi, xj = queue.popleft()
            if self.revise(domain, xi, xj):
                if len(domain[xi]) == 0:
                    return False
                r, c = xi
                for dr, dc in DICHUYEN:
                    nr, nc = r + dr, c + dc
                    if (nr, nc) != xj and 0 <= nr < self.num_rows and 0 <= nc < self.num_cols:
                        queue.append(((nr, nc), xi))
        return True

    # --- Backtracking + AC3 ---
    def backtrack(self, cur, goal, visited, path, domain):
        self.So_tt_daduyet += 1
        self.list_tt_duyet.append(cur)
        visited.add(cur)
        path.append(cur)

        self.Kichthuoc_bonho = max(self.Kichthuoc_bonho, len(path))
        self.Kichthuoc_bonho_MB = max(self.Kichthuoc_bonho_MB, asizeof.asizeof(path)/1024/1024)

        if cur == goal:
            self.duong_di = path.copy()
            self.Dodai_duongdi = len(path)
            return True

        # Tạo domain mới cho bước tiếp theo
        domain_moi = {k:v.copy() for k,v in domain.items()}
        domain_moi[cur] = {1}
        if not self.ac3(domain_moi):
            visited.remove(cur)
            path.pop()
            return False

        # Lọc bước đi hợp lệ
        valid_moves = []
        for dx, dy in DICHUYEN:
            new_x, new_y = cur[0] + dx, cur[1] + dy
            if self.is_valid_move(new_x, new_y, visited):
                valid_moves.append((dx, dy))

        while valid_moves:
            idx = random.randint(0, len(valid_moves)-1)
            dx, dy = valid_moves.pop(idx)
            new_pos = (cur[0]+dx, cur[1]+dy)
            self.So_tt_dasinh += 1
            if self.backtrack(new_pos, goal, visited, path, domain_moi):
                return True

        visited.remove(cur)
        path.pop()
        return False

    def chay_thuattoan(self):
        start_time = time.time()
        start = self.tim_vitri(2)[0]
        goal = self.tim_vitri(3)[0]
        visited = set()
        path = []
        domain = self.tao_domain(visited)

        self.backtrack(start, goal, visited, path, domain)
        self.execution_time = time.time() - start_time
        return self.list_tt_duyet, self.duong_di


# ----- Chạy -----
print("\n", "BacktrackingAC3".center(60, "-"))
solver = BacktrackingAC3()
visited, path = solver.chay_thuattoan()
print("States visited:", [(int(r), int(c)) for r, c in visited])
print("Path:", [(int(r), int(c)) for r, c in path])
print("Stats:", solver.thong_so())

