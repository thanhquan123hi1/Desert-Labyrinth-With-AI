import numpy as np
import time
from pympler import asizeof

# tt: trạng thái
# 2: vị trí nhân vật
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
DICHUYEN = [(-1,0),(0,-1),(0,1),(1,0)]
class DFS:
    def __init__(self, ma_tran=None):
        if ma_tran is None:
            ma_tran = matrix
        self.tt_bandau = np.array(ma_tran)
        self.num_rows, self.num_cols = self.tt_bandau.shape
        self.list_tt_duyet = []
        self.duong_di = []

        # Các thông số để so sánh
        self.So_tt_daduyet = 0  # số trạng thái đã duyệt
        self.So_tt_dasinh = 0  # số trạng thái đã sinh
        self.Kichthuoc_bonho = 0  # Số tt ở thời điểm queue max
        self.Kichthuoc_bonho_MB = 0.0  # kích thước bộ nhớ max
        self.Dodai_duongdi = 0  # chiều dài đường đi
        self.execution_time = 0  # thời gian thực thi

    # 1. Kiểm tra trạng thái có phải goal
    def la_tt_goal(self, row, col):
        return (row, col) == self.tim_vitri(3)[0]

    # 2. Sinh các trạng thái con hợp lệ
    def sinh_tt_con(self, x, y, visited):
        list_tt_con = [] #lưu các tuple(x,y) là vị trí của người chơi
        for i,j in DICHUYEN:
            x1, y1 = x + i, y + j
            if 0 <= x1 <self.num_rows and 0 <= y1 < self.num_cols:
                if self.tt_bandau[x1, y1] != 1 and (x1, y1) not in visited:
                    list_tt_con.append((x1, y1))  # trả về list các vị trí người chơi có thể đi
        return list_tt_con

     # 3. Tìm tập vị trí có giá trị trong ma trận bằng giá trị(cần xét)
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

    # 5. Cập nhật trạng thái bước duyệt
    def luu_tt_daduyet(self, row, col):
        self.list_tt_duyet.append((row, col))

    #6. Thông số
    def thong_so(self):
        return {
            "So tt da duyet": self.So_tt_daduyet,
            "So tt da sinh": self.So_tt_dasinh,
            "Kich thuoc bo nho (tt)": self.Kichthuoc_bonho,
            "Kich thuoc bo nho (MB)": round(self.Kichthuoc_bonho_MB, 6),
            "Do dai duong di": self.Dodai_duongdi,
            "Execution time (s)": round(self.execution_time, 6)
        }

    # --------- Chạy DFS từng bước ----------
    def chay_thuattoan(self):
        start_time = time.time()

        start = self.tim_vitri(2)[0] #Lấy một giá trị tuple đầu
        goal = self.tim_vitri(3)[0]  #Lấy một giá trị tuple đầu
        stack = [start]              #tạo stack vị trí của người chơi
        visited = {start}            #tạo set vị trí của người chơi đã thăm
        cha = {}                     #lưu trạng thái cha để truy vết đường đi

        while stack:
            # Cập nhật kích thước bộ nhớ (theo số trạng thái và MB)
            self.Kichthuoc_bonho = max(self.Kichthuoc_bonho, len(stack))
            stack_size_MB = asizeof.asizeof(stack) / (1024 * 1024)
            self.Kichthuoc_bonho_MB = max(self.Kichthuoc_bonho_MB, stack_size_MB)

            row, col = stack.pop()  # Lấy phần tử cuối (DFS)

            # Cập nhật trạng thái duyệt
            self.luu_tt_daduyet(row, col)
            self.So_tt_daduyet += 1

            # Nếu đến goal, đánh dấu đường đi
            if self.la_tt_goal(row, col):
                self.duong_di = self.tim_duongdi(start, goal, cha)

                self.Dodai_duongdi = len(self.duong_di)
                self.execution_time = time.time() - start_time
                self.execution_time = time.time() - start_time

                self.list_tt_duyet.pop(0)
                self.duong_di.pop(0)
                return self.list_tt_duyet, self.duong_di

            # Sinh trạng thái con và thêm vào stack
            for con in self.sinh_tt_con(row, col, visited):
                visited.add(con)
                cha[con] = (row, col)
                stack.append(con)
                self.So_tt_dasinh += 1

        return self.list_tt_duyet

print("\n","DFS".center(60, "-"))
dfs = DFS()
a, b = dfs.chay_thuattoan()
# ép kiểu tất cả tuple (row, col) trong a và b thành int
a = [(int(row), int(col)) for row, col in a]
b = [(int(row), int(col)) for row, col in b]

print("Trạng thái đã duyệt qua: ", a)
print("Đường đi: ", b)
print("Thông số DFS:", dfs.thong_so())
#Thông số DFS: {
# 'So tt da duyet': 49,
# 'So tt da sinh': 73,
# 'Kich thuoc bo nho (tt)': 26,
# 'Kich thuoc bo nho (MB)': 0.003288,
# 'Do dai duong di': 47,
# 'Execution time (s)': 0.004023
# }






















