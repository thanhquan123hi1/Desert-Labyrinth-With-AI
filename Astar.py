import heapq
import numpy as np
import time
from pympler import asizeof   # để đo bộ nhớ

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
class AStar:
    def __init__(self, ma_tran=None):
        if ma_tran is None:
            ma_tran = matrix
        self.tt_bandau = np.array(ma_tran)
        self.num_rows, self.num_cols = self.tt_bandau.shape
        self.list_tt_duyet = []
        self.duong_di = []

        # Các thông số để so sánh
        self.So_tt_daduyet = 0       # số trạng thái đã duyệt
        self.So_tt_dasinh = 0        # số trạng thái đã sinh
        self.Kichthuoc_bonho = 0     # số tt ở thời điểm queue max
        self.Kichthuoc_bonho_MB = 0.0  # kích thước bộ nhớ max
        self.Dodai_duongdi = 0       # chiều dài đường đi
        self.execution_time = 0      # thời gian thực thi

    # 1. Kiểm tra goal
    def la_tt_goal(self, row, col):
        return (row, col) == self.tim_vitri(3)[0]

    # 2. Sinh trạng thái con
    def sinh_tt_con(self, x, y, visited):
        list_tt_con = []
        for i, j in DICHUYEN:
            x1, y1 = x + i, y + j
            if 0 <= x1 < self.num_rows and 0 <= y1 < self.num_cols:
                if self.tt_bandau[x1, y1] != 1 and (x1, y1) not in visited:
                    list_tt_con.append((x1, y1))
        return list_tt_con

    # 3. Tìm vị trí theo giá trị
    def tim_vitri(self, gia_tri):
        list_toado = np.argwhere(self.tt_bandau == gia_tri)
        return [tuple(p) for p in list_toado]

    # 4. Tìm đường đi
    def tim_duongdi(self, start, goal, cha):
        duong_di = []
        cur = goal
        while cur != start:
            duong_di.append(cur)
            cur = cha[cur]
        duong_di.append(start)
        duong_di.reverse()
        return duong_di

    # 5. Lưu trạng thái duyệt
    def luu_tt_daduyet(self, row, col):
        self.list_tt_duyet.append((row, col))

    # 6. Heuristic Manhattan
    def heuristic(self, vitri):
        goal = self.tim_vitri(3)[0]
        row, col = vitri
        return abs(row - goal[0]) + abs(col - goal[1])

    # 7. Chi phí từ start đến node hiện tại
    def gx(self, parent_g):
        return parent_g + 1

    # 8. Tổng f(x) = g(x) + h(x)
    def fx(self, g, h):
        return g + h

    # 9. Trả về thông số
    def thong_so(self):
        return {
            "So tt da duyet": self.So_tt_daduyet,
            "So tt da sinh": self.So_tt_dasinh,
            "Kich thuoc bo nho (tt)": self.Kichthuoc_bonho,
            "Kich thuoc bo nho (MB)": round(self.Kichthuoc_bonho_MB, 6),
            "Do dai duong di": self.Dodai_duongdi,
            "Execution time (s)": round(self.execution_time, 6)
        }

    # -------- Chạy A* ----------
    def chay_thuattoan(self):
        start_time = time.time()
        start = self.tim_vitri(2)[0]
        goal = self.tim_vitri(3)[0]
        visited = {start}
        g_cost = {start: 0}
        cha = {}

        # priority queue: (f(x), (row, col))
        heap = []
        heapq.heappush(heap, (self.fx(g_cost[start], self.heuristic(start)), start))
        self.So_tt_dasinh += 1
        self.Kichthuoc_bonho = max(self.Kichthuoc_bonho, len(heap))
        self.Kichthuoc_bonho_MB = max(self.Kichthuoc_bonho_MB, asizeof.asizeof(heap) / (1024*1024))

        while heap:
            _, (row, col) = heapq.heappop(heap)
            self.So_tt_daduyet += 1

            # Cập nhật trạng thái duyệt
            self.luu_tt_daduyet(row, col)

            # Nếu đến goal
            if self.la_tt_goal(row, col):
                self.duong_di = self.tim_duongdi(start, goal, cha)
                self.Dodai_duongdi = len(self.duong_di)
                self.Kichthuoc_bonho = max(self.Kichthuoc_bonho, len(heap))
                self.Kichthuoc_bonho_MB = max(self.Kichthuoc_bonho_MB, asizeof.asizeof(heap) / (1024 * 1024))
                self.execution_time = time.time() - start_time

                # Loại bỏ start khỏi danh sách nếu muốn giống Greedy
                self.list_tt_duyet.pop(0)
                self.duong_di.pop(0)
                return self.list_tt_duyet, self.duong_di

            # Sinh trạng thái con
            for con in self.sinh_tt_con(row, col, visited):
                if con in visited:
                    continue
                visited.add(con)
                cha[con] = (row, col)
                g_cost[con] = self.gx(g_cost[(row, col)])
                heapq.heappush(heap, (self.fx(g_cost[con], self.heuristic(con)), con))
                self.So_tt_dasinh += 1

            self.Kichthuoc_bonho = max(self.Kichthuoc_bonho, len(heap))
            self.Kichthuoc_bonho_MB = max(self.Kichthuoc_bonho_MB, asizeof.asizeof(heap) / (1024*1024))

        return None

print("\n","AStar".center(60, "-"))
astar = AStar()
a, b = astar.chay_thuattoan()
# ép kiểu tất cả tuple (row, col) trong a và b thành int
a = [(int(row), int(col)) for row, col in a]
b = [(int(row), int(col)) for row, col in b]

print("Trạng thái đã duyệt qua:   ", a)
print("Đường đi:   ", b)
print("Thông số AStar:", astar.thong_so())
# Thông số AStar: {
# 'So tt da duyet': 145,
# 'So tt da sinh': 159,
# 'Kich thuoc bo nho (tt)': 18,
# 'Kich thuoc bo nho (MB)': 0.003792,
# 'Do dai duong di': 47,
# 'Execution time (s)': 0.015433}
