import numpy as np
from collections import deque
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
DICHUYEN = [(0,1),(1,0),(0,-1),(-1,0)]
class BFS:
    def __init__(self, ma_tran=None):
        if ma_tran is None:
            ma_tran = matrix
        self.tt_bandau = np.array(ma_tran)
        self.num_rows, self.num_cols = self.tt_bandau.shape
        self.list_tt_duyet = []
        self.duong_di = []

        # Các thông số để so sánh
        self.So_tt_daduyet = 0  #số trạng thái đã duyệt
        self.So_tt_dasinh = 0  #số trạng thái đã sinh
        self.Kichthuoc_bonho = 0  #Số tt ở thời điểm queue max
        self.Kichthuoc_bonho_MB = 0.0 #kích thước bộ nhớ max
        self.Dodai_duongdi = 0  #chiều dài đường đi
        self.execution_time = 0  #thời gian thực thi

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
    def luu_tt_daduyet(self,row, col):
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
    # --------- Chạy BFS từng bước ----------
    def chay_thuattoan(self):
        start_time = time.time()

        start = self.tim_vitri(2)[0] #Lấy một giá trị tuple đầu
        goal = self.tim_vitri(3)[0]  #Lấy một giá trị tuple đầu
        queue = deque([start])       #tạo hàng đợi vị trí của người chơi
        visited = {start}            #tạo set vị trí của người chơi đã thăm
        cha = {}                     #lưu lại tt sinh ra tt mới

        while queue:
            self.Kichthuoc_bonho = max(self.Kichthuoc_bonho, len(queue))

            # dùng pympler.asizeof để tính toàn bộ dung lượng queue
            queue_size_MB = asizeof.asizeof(queue) / (1024 * 1024)
            self.Kichthuoc_bonho_MB = max(self.Kichthuoc_bonho_MB, queue_size_MB)

            row, col = queue.popleft()

            # Cập nhật trạng thái duyệt
            self.luu_tt_daduyet(row, col)
            self.So_tt_daduyet += 1

            # Nếu đến goal, đánh dấu đường đi
            if self.la_tt_goal(row, col):
                self.duong_di = self.tim_duongdi(start, goal, cha) #tìm 1 một tập các tuple là đường đi ngắn nhất từ nguồn tới đích

                self.Dodai_duongdi = len(self.duong_di)
                self.execution_time = time.time() - start_time
                self.execution_time = time.time() - start_time

                self.list_tt_duyet.pop(0)
                self.duong_di.pop(0)
                return self.list_tt_duyet, self.duong_di

            # Sinh trạng thái con và thêm vào queue
            for con in self.sinh_tt_con(row, col, visited):
                visited.add(con)
                cha[con] = (row, col)
                queue.append(con)
                self.So_tt_dasinh += 1

        return None


print("\n","BFS".center(60, "-"))
bfs = BFS()
a, b = bfs.chay_thuattoan()
# ép kiểu tất cả tuple (row, col) trong a và b thành int
a = [(int(row), int(col)) for row, col in a]
b = [(int(row), int(col)) for row, col in b]

print("Trạng thái đã duyệt qua:   ", a)
print("Đường đi:   ", b)
print("Thông số BFS:", bfs.thong_so())
#Thông số BFS: {
# 'So tt da duyet': 325,
# 'So tt da sinh': 329,
# 'Kich thuoc bo nho (tt)': 17,
# 'Kich thuoc bo nho (MB)': 0.001228,
# 'Do dai duong di': 47,
# 'Execution time (s)': 0.005887
# }

