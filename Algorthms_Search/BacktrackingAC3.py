# import random
#
# import numpy as np
# import time
# from pympler import asizeof
# from collections import deque
#
# # tt: trạng thái
# # 2: vị trí nhân vật (start)
# # 3: vị trí goal
#
# matrix = [
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
#     [1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1],
#     [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
#     [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
#     [1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
#     [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
#     [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
#     [1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#     [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1],
#     [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
#     [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1],
#     [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1],
#     [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
#     [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 3],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# ]
#
# DICHUYEN = [(0,1),(1,0),(0,-1),(-1,0)]
#
# class BacktrackingAC3:
#     def __init__(self, ma_tran=None):
#         if ma_tran is None:
#             ma_tran = matrix
#         self.tt_bandau = np.array(ma_tran)
#         self.num_rows, self.num_cols = self.tt_bandau.shape
#
#         # lưu thứ tự các trạng thái đã duyệt
#         self.list_tt_duyet = []
#         # lưu đường đi
#         self.duong_di = []
#
#         # Các thông số để so sánh
#         self.So_tt_daduyet = 0  # số trạng thái đã duyệt
#         self.So_tt_dasinh = 0  # số trạng thái đã sinh/được xem xét
#         self.Kichthuoc_bonho = 0  # Số tt ở thời điểm stack max
#         self.Kichthuoc_bonho_MB = 0.0  # kích thước bộ nhớ max
#         self.Dodai_duongdi = 0  # chiều dài đường đi
#         self.execution_time = 0  # thời gian thực thi
#
#     def tim_vitri(self, gia_tri):
#         list_toado = np.argwhere(self.tt_bandau == gia_tri)
#         return [tuple(p) for p in list_toado]
#
#     def thong_so(self):
#         return {
#             "So tt da duyet": self.So_tt_daduyet,
#             "So tt da sinh": self.So_tt_dasinh,
#             "Kich thuoc bo nho (tt)": self.Kichthuoc_bonho,
#             "Kich thuoc bo nho (MB)": round(self.Kichthuoc_bonho_MB, 6),
#             "Do dai duong di": self.Dodai_duongdi,
#             "Execution time (s)": round(self.execution_time, 6)
#         }
#
#     def is_valid_move(self, x, y, visited):
#         if 0 <= x < self.num_rows and 0 <= y < self.num_cols:
#             if self.tt_bandau[x, y] != 1 and (x, y) not in visited:
#                 return True
#         return False
#
#     # --- AC-3 ---
#
#
#     # --- Backtracking + AC3 ---
#     def backtrack(self, cur, goal, visited, path, domain):
#         pass
#
#     def chay_thuattoan(self):
#         pass
#
#
#
# # ----- Chạy -----
# print("\n", "BacktrackingAC3".center(60, "-"))
# solver = BacktrackingAC3()
# visited, path = solver.chay_thuattoan()
# print("States visited:", [(int(r), int(c)) for r, c in visited])
# print("Path:", [(int(r), int(c)) for r, c in path])
# print("Stats:", solver.thong_so())
#
import numpy as np
import time
from pympler import asizeof
from collections import deque

# 1: tường, 2: start, 3: goal
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
        self.list_tt_duyet = []
        self.duong_di = []

        self.So_tt_daduyet = 0
        self.So_tt_dasinh = 0
        self.Kichthuoc_bonho = 0
        self.Kichthuoc_bonho_MB = 0.0
        self.Dodai_duongdi = 0
        self.execution_time = 0

    def tim_vitri(self, gia_tri):
        list_toado = np.argwhere(self.tt_bandau == gia_tri)
        return [tuple(p) for p in list_toado]

    def is_valid(self, r, c):
        return 0 <= r < self.num_rows and 0 <= c < self.num_cols and self.tt_bandau[r][c] != 1

    # Neighbors cho CSP
    def get_neighbors(self, r, c):
        return [(r+dr, c+dc) for dr, dc in DICHUYEN if self.is_valid(r+dr, c+dc)]

    # ----------- AC3 ------------
    def revise(self, domains, Xi, Xj):
        revised = False
        for a in domains[Xi].copy():
            if not any(self.is_consistent(Xi, a, Xj, b) for b in domains[Xj]):
                domains[Xi].remove(a)
                revised = True
        return revised

    def is_consistent(self, Xi, a, Xj, b):
        # Nếu Xi = 1 thì phải có ít nhất một Xj = 1
        if a == 1 and b == 0:
            return False
        return True

    def AC3(self, domains, constraints):
        queue = deque(constraints)
        while queue:
            Xi, Xj = queue.popleft()
            if self.revise(domains, Xi, Xj):
                if not domains[Xi]:
                    return False
                for Xk in self.get_neighbors(*Xi):
                    if Xk != Xj:
                        queue.append((Xk, Xi))
        return True

    # ---------- Backtracking + AC3 -----------
    def backtrack(self, assignment, domains, constraints, goal):
        if len(assignment) == len(domains):
            if assignment[goal] == 1:
                return assignment
            return None

        # Chọn biến chưa gán có domain nhỏ nhất
        unassigned = [v for v in domains if v not in assignment]
        var = min(unassigned, key=lambda v: len(domains[v]))

        for value in domains[var].copy():
            local_domains = {v: set(domains[v]) for v in domains}
            local_domains[var] = {value}
            assignment[var] = value

            if self.AC3(local_domains, constraints):
                result = self.backtrack(assignment, local_domains, constraints, goal)
                if result:
                    return result
            del assignment[var]
        return None

    def chay_thuattoan(self):
        start_time = time.time()
        start = self.tim_vitri(2)[0]
        goal = self.tim_vitri(3)[0]

        variables = [(r, c) for r in range(self.num_rows) for c in range(self.num_cols) if self.tt_bandau[r][c] != 1]
        domains = {v: {0, 1} for v in variables}
        domains[start] = {1}
        domains[goal] = {1}

        constraints = []
        for v in variables:
            for n in self.get_neighbors(*v):
                constraints.append((v, n))

        if not self.AC3(domains, constraints):
            return [], []

        assignment = self.backtrack({}, domains, constraints, goal)
        self.execution_time = time.time() - start_time

        if assignment:
            path = [v for v, val in assignment.items() if val == 1]
            return list(assignment.keys()), path
        else:
            return [], []

    def thong_so(self):
        return {
            "Execution time (s)": round(self.execution_time, 6)
        }


# ----- Chạy -----
print("\n", "BacktrackingAC3".center(60, "-"))
solver = BacktrackingAC3()
visited, path = solver.chay_thuattoan()
print("States visited:", len(visited))
print("Path length:", len(path))
print("Stats:", solver.thong_so())
