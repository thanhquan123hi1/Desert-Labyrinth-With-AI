import numpy as np
import time
from collections import deque
from pympler import asizeof
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
# DI chuyển 4 hướng
DICHUYEN = [(0,1),(1,0),(0,-1),(-1,0)]

class BacktrackingAC3:
    def __init__(self, ma_tran=None, LOOKAHEAD=3):
        self.tt_bandau = np.array(ma_tran if ma_tran is not None else matrix)
        self.num_rows, self.num_cols = self.tt_bandau.shape

        # kết quả và thống kê (giữ theo phong cách BFS)
        self.list_tt_duyet = []   # danh sách tuple (row,col) đã duyệt (dùng để hiển thị states visited theo thứ tự)
        self.duong_di = []        # đường đi (list of tuple) khi tìm thấy goal

        # thống kê
        self.So_tt_daduyet = 0
        self.So_tt_dasinh = 0
        self.Kichthuoc_bonho = 0
        self.Kichthuoc_bonho_MB = 0.0
        self.Dodai_duongdi = 0
        self.execution_time = 0

        # param thuật toán
        self.LOOKAHEAD = max(1, int(LOOKAHEAD))

        # vị trí start/goal cached
        self.start = self.tim_vitri(2)[0]
        self.goal = self.tim_vitri(3)[0]

    # 1. Tìm vị trí có giá trị trong ma trận (giá trị cần xét)
    def tim_vitri(self, gia_tri):
        list_toado = np.argwhere(self.tt_bandau == gia_tri)
        return [tuple(p) for p in list_toado]

    # 2. Kiểm tra ô hợp lệ (trong biên và không phải tường)
    def hop_le(self, row, col):
        return 0 <= row < self.num_rows and 0 <= col < self.num_cols and self.tt_bandau[row, col] != 1

    # 3. Sinh các hàng xóm hợp lệ chưa thăm
    def sinh_tt_con(self, x, y, visited):
        list_tt_con = []
        for i,j in DICHUYEN:
            x1, y1 = x + i, y + j
            if self.hop_le(x1, y1) and (x1, y1) not in visited:
                list_tt_con.append((x1, y1))
        return list_tt_con

    # 4. Tìm đường đi từ start đến goal (từ cha dict)
    def tim_duongdi(self, start, goal, cha):
        duong_di = []
        cur = goal
        while cur != start:
            duong_di.append(cur)
            cur = cha[cur]
        duong_di.append(start)
        duong_di.reverse()
        return duong_di

    # -------- AC-3 và revise cho lookahead domains ----------
    def ac3(self, domains, constraints):
        queue = deque(constraints)
        while queue:
            xi, xj = queue.popleft()
            if self.revise(domains, xi, xj):
                if not domains[xi]:
                    return False
                for xk in domains.keys():
                    if xk != xi and xk != xj:
                        queue.append((xk, xi))
        return True

    def revise(self, domains, xi, xj):
        revised = False
        to_remove = []
        for vi in domains[xi]:
            # kiểm tra có ít nhất 1 u trong domains[xj] sao cho vi và u là adjacent
            ok = False
            for vj in domains[xj]:
                if abs(vi[0] - vj[0]) + abs(vi[1] - vj[1]) == 1:
                    ok = True
                    break
            if not ok:
                to_remove.append(vi)
        for v in to_remove:
            domains[xi].remove(v)
            revised = True
        return revised

    # Tạo domains lookahead cho một node hiện tại
    def build_lookahead_domains(self, current, visited, lookahead):
        domains = {}
        frontier = {current}
        forbidden = set(visited)
        for d in range(1, lookahead+1):
            next_frontier = set()
            candidates = set()
            for (r,c) in frontier:
                for dr,dc in DICHUYEN:
                    nr, nc = r+dr, c+dc
                    if self.hop_le(nr,nc) and (nr,nc) not in forbidden:
                        candidates.add((nr,nc))
                        next_frontier.add((nr,nc))
            domains[f's{d}'] = list(candidates)
            frontier = next_frontier
        return domains

    # -------- Backtracking + AC3 chính ----------
    def chay_thuattoan(self):
        """
        Chạy thuật toán Backtracking + AC3.
        Trả về: self.list_tt_duyet, self.duong_di
        """
        start_time = time.time()
        start = self.start
        goal = self.goal

        # reset stats
        self.list_tt_duyet = []
        self.duong_di = []
        self.So_tt_daduyet = 0
        self.So_tt_dasinh = 0
        self.Kichthuoc_bonho = 0
        self.Kichthuoc_bonho_MB = 0.0
        self.Dodai_duongdi = 0
        self.execution_time = 0

        visited = set()
        cha = {}

        # recursion limit path length to avoid pathological: at most num_rows*num_cols
        MAX_DEPTH = self.num_rows * self.num_cols

        found = self._backtrack(start, visited, cha, start_time, 0, MAX_DEPTH)
        self.execution_time = time.time() - start_time
        if found:
            self.duong_di = self.tim_duongdi(start, goal, cha)
            self.Dodai_duongdi = len(self.duong_di)
        return self.list_tt_duyet, self.duong_di

    def _backtrack(self, current, visited, cha, start_time, depth, MAX_DEPTH):
        # cập nhật thống kê khi "duyệt" node current
        self.list_tt_duyet.append(current)
        self.So_tt_daduyet += 1
        self.Kichthuoc_bonho = max(self.Kichthuoc_bonho, depth+1)
        queue_size_MB = asizeof.asizeof(self.list_tt_duyet) / (1024 * 1024)
        self.Kichthuoc_bonho_MB = max(self.Kichthuoc_bonho_MB, queue_size_MB)

        # nếu đến goal
        if current == self.goal:
            return True

        if depth >= MAX_DEPTH:
            return False

        visited.add(current)

        # Sinh các hành động (neighbors) theo phong cách bạn dùng
        neighbors = self.sinh_tt_con(current[0], current[1], visited)
        # Lọc: có thể shuffle để random (càng giống backtracking 8 con xe).

        for nb in neighbors:
            # tăng số trạng thái đã sinh
            self.So_tt_dasinh += 1


            domains = self.build_lookahead_domains(nb, visited | {nb}, self.LOOKAHEAD)

            inconsistent = any(len(domains[k]) == 0 for k in domains)
            if inconsistent:

                continue

            constraints = []
            keys = sorted(domains.keys(), key=lambda x: int(x[1:]))
            for i in range(len(keys)-1):
                constraints.append((keys[i], keys[i+1]))
                constraints.append((keys[i+1], keys[i]))  # hai chiều để mạnh hơn


            domains_copy = {k: v.copy() for k,v in domains.items()}
            ac3_ok = True
            if constraints:
                ac3_ok = self.ac3(domains_copy, constraints)

            if not ac3_ok:
                # prune neighbor nb
                continue

            # Nếu AC3 cho phép, tiếp tục đi sâu
            cha[nb] = current
            found = self._backtrack(nb, visited, cha, start_time, depth+1, MAX_DEPTH)
            if found:
                return True
            # quay lui
            del cha[nb]
            # tiếp tục thử neighbor khác

        visited.remove(current)
        # Nếu không tìm thấy từ current, quay lui
        return False

    # Thông số trả về giống BFS
    def thong_so(self):
        return {
            "So tt da duyet": self.So_tt_daduyet,
            "So tt da sinh": self.So_tt_dasinh,
            "Kich thuoc bo nho (tt)": self.Kichthuoc_bonho,
            "Kich thuoc bo nho (MB)": round(self.Kichthuoc_bonho_MB, 6),
            "Do dai duong di": self.Dodai_duongdi,
            "Execution time (s)": round(self.execution_time, 6)
        }


mb = BacktrackingAC3(LOOKAHEAD=3)
a, b = mb.chay_thuattoan()
# ép kiểu tuple sang int giống BFS (thường đã là int)
a = [(int(r), int(c)) for r,c in a]
b = [(int(r), int(c)) for r,c in b]
print("Trạng thái đã duyệt qua: ", a)
print("Đường đi: ", b)
print("Thông số:", mb.thong_so())
