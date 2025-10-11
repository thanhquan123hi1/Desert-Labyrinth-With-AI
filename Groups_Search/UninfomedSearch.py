import numpy as np
import time
from collections import deque

DICHUYEN = [(-1, 0), (0, -1), (0, 1), (1, 0)]

class UninformedSearch:
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

    def sinh_tt_con(self, x, y, visited):
        list_tt_con = []
        for i, j in DICHUYEN:
            x1, y1 = x + i, y + j
            if 0 <= x1 < self.num_rows and 0 <= y1 < self.num_cols:
                if self.tt_bandau[x1, y1] != 1 and (x1, y1) not in visited:
                    list_tt_con.append((x1, y1))
        return list_tt_con

    def tim_duongdi(self, start, goal, cha):
        path = []
        cur = goal
        while cur != start:
            path.append(cur)
            cur = cha[cur]
        path.append(start)
        path.reverse()
        return path

    def thong_so(self):
        return {
            "Số trạng thái đã duyệt: ": self.So_tt_daduyet,
            "Số trạng thái đã sinh: ": self.So_tt_dasinh,
            "Độ dài đường đi: ": self.Dodai_duongdi,
            "Thời gian chạy (s): ": round(self.execution_time, 6)
        }

    def DFS(self):
        self.reset_stats()
        start_time = time.time()
        start, goal = self.start, self.goal
        stack = [start]
        visited = {start}
        cha = {}

        while stack:
            row, col = stack.pop()
            self.list_tt_duyet.append((row, col))
            self.So_tt_daduyet += 1

            if (row, col) == goal:
                self.duong_di = self.tim_duongdi(start, goal, cha)
                self.Dodai_duongdi = len(self.duong_di)
                self.execution_time = time.time() - start_time
                return self.list_tt_duyet, self.duong_di

            for con in self.sinh_tt_con(row, col, visited):
                visited.add(con)
                cha[con] = (row, col)
                stack.append(con)
                self.So_tt_dasinh += 1

        self.execution_time = time.time() - start_time
        return self.list_tt_duyet, []

    def BFS(self):
        self.reset_stats()
        start_time = time.time()
        start, goal = self.start, self.goal
        queue = deque([start])
        visited = {start}
        cha = {}

        while queue:
            row, col = queue.popleft()
            self.list_tt_duyet.append((row, col))
            self.So_tt_daduyet += 1

            if (row, col) == goal:
                self.duong_di = self.tim_duongdi(start, goal, cha)
                self.Dodai_duongdi = len(self.duong_di)
                self.execution_time = time.time() - start_time
                return self.list_tt_duyet, self.duong_di

            for con in self.sinh_tt_con(row, col, visited):
                visited.add(con)
                cha[con] = (row, col)
                queue.append(con)
                self.So_tt_dasinh += 1

        self.execution_time = time.time() - start_time
        return self.list_tt_duyet, []
