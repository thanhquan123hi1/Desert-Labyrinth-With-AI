import random

import numpy as np
import time
from pympler import asizeof
from collections import deque

#tt: trạng thái
#2: vị trí nhân vật (start)
#3: vị trí goal
#Biến là vị trí hiện tại --> chỉ có 1 biến
#Giá trị là các ô có thể đi tiếp theo(4 hướng)
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

class BacktrackingForwardChecking:
    def __init__(self, ma_tran=None):
        if ma_tran is None:
            ma_tran = matrix
        self.tt_bandau = np.array(ma_tran)
        self.num_rows, self.num_cols = self.tt_bandau.shape

        #lưu thứ tự các trạng thái đã duyệt
        self.list_tt_duyet = []
        #lưu đường đi
        self.duong_di = []

        #Các thông số để so sánh
        self.So_tt_daduyet = 0  #số trạng thái đã duyệt
        self.So_tt_dasinh = 0   #số trạng thái đã sinh/được xem xét
        self.Kichthuoc_bonho = 0  #Số tt ở thời điểm stack max
        self.Kichthuoc_bonho_MB = 0.0 #kích thước bộ nhớ max
        self.Dodai_duongdi = 0  #chiều dài đường đi
        self.execution_time = 0  #thời gian thực thi

    #1. Tìm tập vị trí có giá trị trong ma trận bằng giá trị
    def tim_vitri(self, gia_tri):
        list_toado = np.argwhere(self.tt_bandau == gia_tri)
        return [tuple(p) for p in list_toado]

    #2. Thông số
    def thong_so(self):
        return {
            "So tt da duyet": self.So_tt_daduyet,
            "So tt da sinh": self.So_tt_dasinh,
            "Kich thuoc bo nho (tt)": self.Kichthuoc_bonho,
            "Kich thuoc bo nho (MB)": round(self.Kichthuoc_bonho_MB, 6),
            "Do dai duong di": self.Dodai_duongdi,
            "Execution time (s)": round(self.execution_time, 6)
        }

    #3.Kiểm tra ràng buộc + Forward Checking
    def is_valid_move(self, x, y, visited):
        if 0 <= x < self.num_rows and 0 <= y < self.num_cols: #nằm trong mê cung
            if self.tt_bandau[x, y] != 1 and (x, y) not in visited: #ko đụng tường và đã đi qua
                return True
        return False

    #4.Backtracking đệ quy với forward checking
    def backtrack(self, cur, goal, visited, path):
        self.So_tt_daduyet += 1
        self.list_tt_duyet.append(cur)
        visited.add(cur)
        path.append(cur)

        #Cập nhật kích thước bộ nhớ và stack max
        self.Kichthuoc_bonho = max(self.Kichthuoc_bonho, len(path))
        self.Kichthuoc_bonho_MB = max(self.Kichthuoc_bonho_MB, asizeof.asizeof(path) / 1024 / 1024)

        if cur == goal:
            self.duong_di = path.copy()
            self.Dodai_duongdi = len(path)
            return True

        #Lọc trước các bước đi hợp lệ
        valid_moves = []
        for dx, dy in DICHUYEN:
            new_x, new_y = cur[0] + dx, cur[1] + dy
            if self.is_valid_move(new_x, new_y, visited):
                valid_moves.append((dx, dy))

        #Random từng bước đi trong số các bước hợp lệ
        while valid_moves:
            random.seed(43)
            idx = random.randint(0, len(valid_moves) - 1)
            dx, dy = valid_moves.pop(idx)
            new_x, new_y = cur[0] + dx, cur[1] + dy
            self.So_tt_dasinh += 1
            if self.backtrack((new_x, new_y), goal, visited, path):
                return True

        #Quay lui
        visited.remove(cur)
        path.pop()
        return False

    #---------- Chạy BacktrackingForwardChecking ----------
    def chay_thuattoan(self):
        start_time = time.time()
        start = self.tim_vitri(2)[0]
        goal = self.tim_vitri(3)[0]
        visited = set()
        path = []

        self.backtrack(start, goal, visited, path)
        self.execution_time = time.time() - start_time

        self.list_tt_duyet.pop(0)
        self.duong_di.pop(0)
        return self.list_tt_duyet, self.duong_di


print("\n", "BacktrackingForwardChecking".center(60, "-"))
btk = BacktrackingForwardChecking()
a, b = btk.chay_thuattoan()

#ép kiểu tất cả tuple (row, col) trong a và b thành int
a = [(int(row), int(col)) for row, col in a]
b = [(int(row), int(col)) for row, col in b]

print("Trạng thái đã duyệt qua:   ", a)
print("Đường đi:   ", b)
print("Thông số:", btk.thong_so())
# Thông số: {
# 'So tt da duyet': 57,
# 'So tt da sinh': 56,
# 'Kich thuoc bo nho (tt)': 51,
# 'Kich thuoc bo nho (MB)': 0.006302,
# 'Do dai duong di': 51,
# 'Execution time (s)': 0.007595
# }
