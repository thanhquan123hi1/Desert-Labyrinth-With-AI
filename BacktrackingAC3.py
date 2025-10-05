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
