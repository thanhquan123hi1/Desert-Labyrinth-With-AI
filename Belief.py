import numpy as np
from collections import deque
import time
from pympler import asizeof

# Ma trận game: 1=wall, 0=free, 2=start, 3=goal
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
    [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3]
]

DICHUYEN = [(0,1),(1,0),(0,-1),(-1,0)]  # phải, xuống, trái, lên

class Belief:
    """Phiên bản 'belief' cho game ma trận"""
    def __init__(self, ma_tran=None):
        if ma_tran is None:
            ma_tran = matrix
        self.ma_tran = np.array(ma_tran)
        self.num_rows, self.num_cols = self.ma_tran.shape
        self.list_tt_duyet = []
        self.duong_di = []
        # Thống kê
        self.So_tt_daduyet = 0
        self.So_tt_dasinh = 0
        self.Kichthuoc_bonho = 0
        self.Kichthuoc_bonho_MB = 0.0
        self.Dodai_duongdi = 0
        self.execution_time = 0

        # Start position
        start_positions = list(map(tuple, np.argwhere(self.ma_tran==2)))
        self.start = start_positions[0]
        # Goal position
        goal_positions = list(map(tuple, np.argwhere(self.ma_tran==3)))
        self.goal = goal_positions[0]

    # Kiểm tra trạng thái goal
    def la_tt_goal(self, pos):
        return pos == self.goal

    # Sinh các trạng thái con hợp lệ
    def sinh_tt_con(self, pos, visited):
        list_tt_con = []
        x, y = pos
        for dx, dy in DICHUYEN:
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.num_rows and 0 <= ny < self.num_cols:
                if self.ma_tran[nx, ny] != 1 and (nx, ny) not in visited:
                    list_tt_con.append((nx, ny))
        return list_tt_con

    # Belief search kiểu DFS
    def chay_thuattoan(self):
        start_time = time.time()
        stack = [self.start]
        visited = {self.start}
        cha = {}

        while stack:
            pos = stack.pop()
            self.list_tt_duyet.append(pos)
            self.So_tt_daduyet += 1

            if self.la_tt_goal(pos):
                # Tạo đường đi từ cha
                path = []
                cur = pos
                while cur != self.start:
                    path.append(cur)
                    cur = cha[cur]
                path.append(self.start)
                path.reverse()
                self.duong_di = path
                self.Dodai_duongdi = len(path)
                self.execution_time = time.time() - start_time
                return self.list_tt_duyet, self.duong_di

            # Sinh trạng thái con
            for con in self.sinh_tt_con(pos, visited):
                visited.add(con)
                cha[con] = pos
                stack.append(con)
                self.So_tt_dasinh += 1

            # Cập nhật bộ nhớ
            self.Kichthuoc_bonho = max(self.Kichthuoc_bonho, len(stack))
            self.Kichthuoc_bonho_MB = max(self.Kichthuoc_bonho_MB,
                                          asizeof.asizeof(stack)/(1024*1024))
        self.execution_time = time.time() - start_time
        return None

    # Thống số thuật toán
    def thong_so(self):
        return {
            "So tt da duyet": self.So_tt_daduyet,
            "So tt da sinh": self.So_tt_dasinh,
            "Kich thuoc bo nho (tt)": self.Kichthuoc_bonho,
            "Kich thuoc bo nho (MB)": round(self.Kichthuoc_bonho_MB, 6),
            "Do dai duong di": self.Dodai_duongdi,
            "Execution time (s)": round(self.execution_time, 6)
        }
bm = Belief()
a, b = bm.chay_thuattoan()
print("Trạng thái đã duyệt qua:", a)
print("Đường đi:", b)
print("Thông số:", bm.thong_so())


