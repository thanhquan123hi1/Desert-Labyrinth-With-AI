import numpy as np
import time
from pympler import asizeof  # để đo bộ nhớ

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
BEAM = 5

class BeamSearch:
    def __init__(self, ma_tran=None):
        if ma_tran is None:
            ma_tran = matrix
        self.tt_bandau = np.array(ma_tran)
        self.num_rows, self.num_cols = self.tt_bandau.shape

        self.beam = BEAM

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

    # 1. Kiểm tra trạng thái có phải goal
    def la_tt_goal(self, row, col):
        return (row, col) == self.tim_vitri(3)[0]

    # 2. Sinh các trạng thái con hợp lệ
    def sinh_tt_con(self, x, y, visited):
        list_tt_con = []
        for i,j in DICHUYEN:
            x1, y1 = x + i, y + j
            if 0 <= x1 <self.num_rows and 0 <= y1 < self.num_cols:
                if self.tt_bandau[x1, y1] != 1 and (x1, y1) not in visited:
                    list_tt_con.append((x1, y1))
        return list_tt_con

    # 3. Tìm tập vị trí có giá trị trong ma trận bằng giá trị
    def tim_vitri(self, gia_tri):
        list_toado = np.argwhere(self.tt_bandau == gia_tri)
        return [tuple(p) for p in list_toado]

    # 4. Tìm đường đi từ start đến goal
    def tim_duongdi(self, start, goal, cha):
        duong_di = []
        cur = goal
        while cur != start:
            duong_di.append(cur)
            cur = cha[cur]
        duong_di.append(start)
        duong_di.reverse()
        return duong_di

    # 5. Lưu trạng thái bước duyệt
    def luu_tt_daduyet(self, row, col):
        self.list_tt_duyet.append((row, col))

    # 6. Heuristic Manhattan
    def heuristic(self, vitri):
        goal = self.tim_vitri(3)[0]
        row, col = vitri
        return abs(row - goal[0]) + abs(col - goal[1])

    # 7. Trả về thông số
    def thong_so(self):
        return {
            "So tt da duyet": self.So_tt_daduyet,
            "So tt da sinh": self.So_tt_dasinh,
            "Kich thuoc bo nho (tt)": self.Kichthuoc_bonho,
            "Kich thuoc bo nho (MB)": round(self.Kichthuoc_bonho_MB, 6),
            "Do dai duong di": self.Dodai_duongdi,
            "Execution time (s)": round(self.execution_time, 6)
        }

    # --------- Chạy BeamSearch từng bước ----------
    def chay_thuattoan(self):
        start_time = time.time()
        start = self.tim_vitri(2)[0]
        goal = self.tim_vitri(3)[0]
        visited = {start}
        cha = {}

        list_ungvien = [(start, cha)]

        self.So_tt_dasinh += 1
        self.Kichthuoc_bonho = max(self.Kichthuoc_bonho, len(list_ungvien))
        self.Kichthuoc_bonho_MB = max(self.Kichthuoc_bonho_MB, asizeof.asizeof(list_ungvien)/(1024*1024))

        while list_ungvien:
            tmp_lst = []

            for toado, cha_curr in list_ungvien:
                row, col = toado
                self.So_tt_daduyet += 1
                self.luu_tt_daduyet(row, col)

                if self.la_tt_goal(row, col):
                    self.duong_di = self.tim_duongdi(start, goal, cha_curr)
                    self.Dodai_duongdi = len(self.duong_di)
                    self.execution_time = time.time() - start_time
                    self.Kichthuoc_bonho = max(self.Kichthuoc_bonho, len(list_ungvien))
                    self.Kichthuoc_bonho_MB = max(self.Kichthuoc_bonho_MB, asizeof.asizeof(list_ungvien)/(1024*1024))
                    self.list_tt_duyet.pop(0)
                    self.duong_di.pop(0)
                    return self.list_tt_duyet, self.duong_di

                for con in self.sinh_tt_con(row, col, visited):
                    visited.add(con)
                    new_cha = cha_curr.copy()
                    new_cha[con] = (row, col)
                    tmp_lst.append((con, new_cha))
                    self.So_tt_dasinh += 1

            if not tmp_lst:
                return None

            tmp_lst.sort(key=lambda x: self.heuristic(x[0]))
            list_ungvien = tmp_lst[:self.beam]

            self.Kichthuoc_bonho = max(self.Kichthuoc_bonho, len(list_ungvien))
            self.Kichthuoc_bonho_MB = max(self.Kichthuoc_bonho_MB, asizeof.asizeof(list_ungvien)/(1024*1024))

        return None




print("\n", "BeamSearch".center(60, "-"))
beamsearch = BeamSearch()
a, b = beamsearch.chay_thuattoan()
# ép kiểu tất cả tuple (row, col) trong a và b thành int
a = [(int(row), int(col)) for row, col in a]
b = [(int(row), int(col)) for row, col in b]

print("Trạng thái đã duyệt qua:   ", a)
print("Đường đi:   ", b)
print("Thông số BeamSearch:", beamsearch.thong_so())
# Thông số BeamSearch: {
# 'So tt da duyet': 171,
# 'So tt da sinh': 178,
# 'Kich thuoc bo nho (tt)': 5,
# 'Kich thuoc bo nho (MB)': 0.018242,
# 'Do dai duong di': 47,
# 'Execution time (s)': 0.016067
# }