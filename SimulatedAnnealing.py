import heapq
import math
import random
import time
import numpy as np
from pympler import asizeof  # để đo bộ nhớ

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
class SimulatedAnnealing:
    def __init__(self, ma_tran = None, T_init=50, alpha=0.8):
        if ma_tran is None:
            ma_tran = matrix
        self.tt_bandau = np.array(ma_tran)
        self.num_rows, self.num_cols = self.tt_bandau.shape
        self.list_tt_duyet = []
        self.duong_di = []
        self.visited = set()

        self.T_init = T_init
        self.alpha = alpha

        # Các thông số để so sánh
        self.So_tt_daduyet = 0       # số trạng thái đã duyệt
        self.So_tt_dasinh = 0        # số trạng thái đã sinh
        self.Kichthuoc_bonho = 0     # số tt ở thời điểm queue max
        self.Kichthuoc_bonho_MB = 0.0  # kích thước bộ nhớ max
        self.Dodai_duongdi = 0       # chiều dài đường đi
        self.execution_time = 0      # thời gian thực thi

    # 1. Kiểm tra trạng thái có phải goal
    def la_tt_goal(self, row, col):
        return (row, col) == self.tim_vitri(3)[0]

    # 2. Sinh các trạng thái con hợp lệ
    def sinh_tt_con(self, x, y, visited):
        list_tt_con = [] #lưu các tuple(x,y) là vị trí của người chơi
        for i,j in DICHUYEN:
            x1, y1 = x + i, y + j
            if 0 <= x1 < self.num_rows and 0 <= y1 < self.num_cols:
                if self.tt_bandau[x1, y1] != 1 and (x1, y1) not in self.visited:
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
        self.So_tt_daduyet += 1

    # 6. Tính khoảng cách Manhattan từ toạ độ tới goal
    def heuristic(self, pos):
        goal = self.tim_vitri(3)[0]
        start = pos

        heap = [(0, start)]
        g_cost = {start: 0}
        visited = set().union(self.visited)

        while heap:
            _, node = heapq.heappop(heap)
            if node == goal:
                return g_cost[node] + abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
            if node in visited:
                continue
            visited.add(node)
            row, col = node
            for dr, dc in DICHUYEN:
                r, c = row + dr, col + dc
                if 0 <= r < self.num_rows and 0 <= c < self.num_cols:
                    if self.tt_bandau[r, c] != 1:
                        cost = g_cost[node] + 1
                        if (r, c) not in g_cost or cost < g_cost[(r, c)]:
                            g_cost[(r, c)] = cost
                            h = abs(r - goal[0]) + abs(c - goal[1])  # Manhattan cho sắp xếp heap
                            heapq.heappush(heap, (cost + h, (r, c)))
        return float('inf')

    # 7. Hàm tính nhiệt độ theo độ sâu
    def NhietDoT(self, dosau):
        return self.T_init * (self.alpha ** dosau)

    # 8. Hàm tính xác suất chấp nhận trạng thái tệ hơn
    def Xacsuat_chapnhan(self, delta_h, T):
        return math.exp(-abs(delta_h) / T) if T > 0 else 0

    # 9. Thông số
    def thong_so(self):
        return {
            "So tt da duyet": self.So_tt_daduyet,
            "So tt da sinh": self.So_tt_dasinh,
            "Kich thuoc bo nho (tt)": self.Kichthuoc_bonho,
            "Kich thuoc bo nho (MB)": round(self.Kichthuoc_bonho_MB, 6),
            "Do dai duong di": self.Dodai_duongdi,
            "Execution time (s)": round(self.execution_time, 6)
        }

    # --------- Chạy SimulatedAnnealing từng bước ----------
    def chay_thuattoan(self):
        start_time = time.time()

        start = self.tim_vitri(2)[0]  # vị trí bắt đầu

        H = start  # trạng thái hiện tại
        cha = {}  # lưu truy vết đường đi
        self.visited = {H}  # đánh dấu các vị trí đã đi

        self.list_tt_duyet.append(start)
        dosau = 0
        accept = True
        queue = []
        while True:
            row, col = H
            # Nếu tới goal thì lưu đường đi và kết thúc
            if self.la_tt_goal(row, col):
                self.duong_di = self.tim_duongdi(start, H, cha)
                self.Dodai_duongdi = len(self.duong_di)
                self.execution_time = time.time() - start_time
                self.list_tt_duyet.pop(0)
                self.duong_di.pop(0)
                return self.list_tt_duyet, self.duong_di

            # Tính nhiệt độ
            T = self.NhietDoT(dosau)
            if T < 1e-100:  # nhiệt độ quá thấp → dừng
                break

            # Sinh các trạng thái lân cận chưa đi
            queue = self.sinh_tt_con(row, col, self.visited)

            self.So_tt_dasinh += len(queue)
            self.Kichthuoc_bonho = max(self.Kichthuoc_bonho, len(queue))
            self.Kichthuoc_bonho_MB = max(self.Kichthuoc_bonho_MB, asizeof.asizeof(queue)/(1024*1024))

            if not queue:  # nếu không còn trạng thái con thì dừng
                break

            # Tìm trạng thái tốt nhất M
            heuristics = [self.heuristic(pos) for pos in queue]
            i_mincost = np.argmin(heuristics)
            M = queue[i_mincost]

            delta_h = self.heuristic(M) - self.heuristic(H)
            # Chấp nhận trạng thái con
            accept = False
            if delta_h < 0:
                accept = True
            else:
                P = self.Xacsuat_chapnhan(delta_h, T)
                rp = random.uniform(0, 1)
                if rp > P:
                    accept = True
            if accept:
                cha[M] = H
                H = M
                self.visited.add(H)
                self.luu_tt_daduyet(H[0], H[1])

            dosau += 1  # tăng độ sâu để giảm T
        self.execution_time = time.time() - start_time
        return self.list_tt_duyet, self.duong_di


print("\n", "SimulatedAnnealing".center(60, "-"))
simulatedannealing = SimulatedAnnealing()
a, b = simulatedannealing.chay_thuattoan()
# ép kiểu tất cả tuple (row, col) trong a và b thành int
a = [(int(row), int(col)) for row, col in a]
b = [(int(row), int(col)) for row, col in b]

print("Trạng thái đã duyệt qua:   ", a)
print("Đường đi:   ", b)
print("Thông số SimulatedAnnealing:", simulatedannealing.thong_so())
# Thông số SimulatedAnnealing: {
# 'So tt da duyet': 46,
# 'So tt da sinh': 71,
# 'Kich thuoc bo nho (tt)': 3,
# 'Kich thuoc bo nho (MB)': 0.000443,
# 'Do dai duong di': 47,
# 'Execution time (s)': 0.018888
# }