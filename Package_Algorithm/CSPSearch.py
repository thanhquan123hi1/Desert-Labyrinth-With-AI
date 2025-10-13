import random
import numpy as np
import time

DICHUYEN = [(0,1),(1,0),(0,-1),(-1,0)]

class CSPSearch:
    def __init__(self, map_model, start=(1, 1), goal=(19, 28)):

        self.map_model = map_model
        self.tt_bandau = np.array(map_model.collision_matrix)
        self.num_rows, self.num_cols = self.tt_bandau.shape
        self.start = start
        self.goal = goal
        self.reset_stats()

    def reset_stats(self):
        self.list_tt_duyet = []
        self.duong_di = []
        self.So_tt_daduyet = 0
        self.So_tt_dasinh = 0
        self.Dodai_duongdi = 0
        self.execution_time = 0

    def thong_so(self):
        success = len(self.duong_di) > 0
        return {
            "Kết quả": "Thành công" if success else "Thất bại",
            "Số trạng thái đã duyệt": self.So_tt_daduyet,
            "Số trạng thái đã sinh": self.So_tt_dasinh,
            "Độ dài đường đi": self.Dodai_duongdi,
            "Thời gian chạy (s)": round(self.execution_time, 6),
        }

    #Kiểm tra ràng buộc
    def is_valid_move(self, x, y, visited):
        if 0 <= x < self.num_rows and 0 <= y < self.num_cols: #nằm trong mê cung
            if self.tt_bandau[x, y] != 1 and (x, y) not in visited: #ko đụng tường và đã đi qua
                return True
        return False

    #---------- Chạy thuật toán BacktrackingForwardChecking ----------
    #Backtracking đệ quy với forward checking
    def Backtrack(self, cur, goal, visited, path):
        self.So_tt_daduyet += 1
        self.list_tt_duyet.append(cur)
        visited.add(cur)
        path.append(cur)

        if cur == goal:
            self.duong_di = path.copy()
            self.Dodai_duongdi = len(path)
            return True

        valid_moves = [] #Lọc trước các bước đi hợp lệ
        for dx, dy in DICHUYEN:
            new_x, new_y = cur[0] + dx, cur[1] + dy
            if self.is_valid_move(new_x, new_y, visited):
                valid_moves.append((dx, dy))

        while valid_moves: #Random từng bước đi trong số các bước hợp lệ
            random.seed(43)
            idx = random.randint(0, len(valid_moves) - 1)
            dx, dy = valid_moves.pop(idx)
            new_x, new_y = cur[0] + dx, cur[1] + dy
            self.So_tt_dasinh += 1
            if self.Backtrack((new_x, new_y), goal, visited, path):
                return True

        #Quay lui
        visited.remove(cur)
        path.pop()
        return False

    def ForwardChecking(self):
        self.reset_stats()
        start_time = time.time()
        start, goal = self.start, self.goal
        visited = set()
        path = []

        self.Backtrack(start, goal, visited, path)

        self.execution_time = time.time() - start_time
        return self.list_tt_duyet, self.duong_di
