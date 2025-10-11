import heapq
import numpy as np
import time

DICHUYEN = [(-1, 0), (0, -1), (0, 1), (1, 0)]

class InformedSearch:
    def __init__(self, map_model, start=(1,1), goal=(19,28)):
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

    #Hàm Heuristic theo Manhattan + lookedhead_penalty + Dead-end_penalty
    def lookahead_penalty(self, row, col, depth, visited=None, weight=1.0):
        visited = visited or set() # Khi mới vào hàm lookahead_penalty

        if not depth: return 0 # Kết thúc đệ quy

        visited.add((row, col))
        moves = []

        for dr, dc in DICHUYEN:
            r1, c1 = row + dr, col + dc
            if 0 <= r1 < self.num_rows and 0 <= c1 < self.num_cols:
                if self.tt_bandau[r1, c1] != 1 and (r1, c1) not in visited:
                    moves.append((r1, c1))

        if len(moves) == 0: # penalty theo số bước có thể đi hiện tại
            penalty = 10 * weight
        elif len(moves) == 1:
            penalty = 1 * weight
        else:
            penalty = 0

        if moves: # đệ quy lookahead, giảm độ sâu
            next_penalties = [self.lookahead_penalty(r1, c1, depth - 1, visited.copy(), weight * 0.6) for r1, c1 in moves]
            penalty += max(next_penalties) # chọn nhánh tệ nhất
        return penalty

    def heuristic(self, vitri, lookahead_steps=3):
        row, col = vitri
        goal = self.goal

        manhattan = abs(row - goal[0]) + abs(col - goal[1]) # Manhattan

        moves_now = sum(1 for dr, dc in DICHUYEN # Dead-end penalty
            if 0 <= row + dr < self.num_rows and 0 <= col + dc < self.num_cols and self.tt_bandau[row + dr, col + dc] != 1)
        if moves_now == 0:
            dead_end_penalty = 10
        elif moves_now == 1:
            dead_end_penalty = 1
        else:
            dead_end_penalty = 0

        lookahead_pen = self.lookahead_penalty(row, col, lookahead_steps) # Lookahead penalty

        return manhattan + dead_end_penalty + lookahead_pen # Heuristic tổng (h càng nhỏ càng tốt)

    # Hàm fx = gx +hx
    def gx(self, parent_g):
        return parent_g + 1
    def fx(self, g, h):
        return g + h

    #--------Chạy thuật toán--------
    def Greedy(self):
        self.reset_stats()
        start_time = time.time()
        start, goal = self.start, self.goal
        visited = {start}
        cha = {}
        heap = []

        heapq.heappush(heap, (self.heuristic(start), start))
        self.So_tt_dasinh += 1

        while heap:
            _, (row, col) = heapq.heappop(heap)
            self.So_tt_daduyet += 1
            self.list_tt_duyet.append((row, col))

            if (row, col) == goal:
                self.duong_di = self.tim_duongdi(start, goal, cha)
                self.Dodai_duongdi = len(self.duong_di)
                self.execution_time = time.time() - start_time
                return self.list_tt_duyet, self.duong_di

            # Sinh trạng thái con
            for con in self.sinh_tt_con(row, col, visited):
                visited.add(con)
                cha[con] = (row, col)
                heapq.heappush(heap, (self.heuristic(con), con))
                self.So_tt_dasinh += 1

        self.execution_time = time.time() - start_time
        return self.list_tt_duyet, []

    def Astar(self):
        self.reset_stats()
        start_time = time.time()
        start, goal = self.start, self.goal
        visited = {start}
        cha = {}
        g_cost = {start: 0}

        heap = []
        heapq.heappush(heap, (self.fx(g_cost[start], self.heuristic(start)), start))
        self.So_tt_dasinh += 1

        while heap:
            _, (row, col) = heapq.heappop(heap)
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
                g_cost[con] = self.gx(g_cost[(row, col)])
                heapq.heappush(heap, (self.fx(g_cost[con], self.heuristic(con)), con))
                self.So_tt_dasinh += 1

        self.execution_time = time.time() - start_time

