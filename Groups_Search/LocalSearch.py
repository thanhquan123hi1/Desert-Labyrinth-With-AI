import heapq
import math
import random

import numpy as np
import time

DICHUYEN = [(-1, 0), (0, -1), (0, 1), (1, 0)]
BEAM = 5
T_INIT=50
ALPHA=0.8

class LocalSearch:
    def __init__(self, map_model, start=(1, 1), goal=(19, 28)):

        self.map_model = map_model
        self.tt_bandau = np.array(map_model.collision_matrix)
        self.num_rows, self.num_cols = self.tt_bandau.shape
        self.start = start
        self.goal = goal
        self.beam = BEAM #Bean
        self.T_init = T_INIT #SimulatedAnnealing
        self.alpha = ALPHA
        self.visited = set()
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

    #-------Chạy thuật toán BeamSearch-------
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

    def BeamSearch(self):
        self.reset_stats()
        start_time = time.time()
        start, goal = self.start, self.goal
        visited = {start}
        cha = {}

        list_ungvien = [(start, cha)]
        self.So_tt_dasinh += 1

        while list_ungvien:
            tmp_lst = []

            for toado, cha_curr in list_ungvien:
                row, col = toado
                self.list_tt_duyet.append((row, col))
                self.So_tt_daduyet += 1

                if (row, col) == goal:
                    self.duong_di = self.tim_duongdi(start, goal, cha_curr)
                    self.Dodai_duongdi = len(self.duong_di)
                    self.execution_time = time.time() - start_time
                    return self.list_tt_duyet, self.duong_di

                for con in self.sinh_tt_con(row, col, visited):
                    visited.add(con)
                    new_cha = cha_curr.copy()
                    new_cha[con] = (row, col)
                    tmp_lst.append((con, new_cha))
                    self.So_tt_dasinh += 1

            if not tmp_lst:
                return self.list_tt_duyet, []

            tmp_lst.sort(key=lambda x: self.heuristic(x[0]))
            list_ungvien = tmp_lst[:self.beam]

        self.execution_time = time.time() - start_time
        return self.list_tt_duyet, []

    # -------Chạy thuật toán SimulatedAnnealing-------
    #Hàm tính nhiệt độ theo độ sâu
    def NhietDoT(self, dosau):
        return self.T_init * (self.alpha ** dosau)

    #Hàm tính xác suất chấp nhận trạng thái tệ hơn
    def Xacsuat_chapnhan(self, delta_h, T):
        return math.exp(-abs(delta_h) / T) if T > 0 else 0

    def heuristic_SA(self, pos):
        goal = self.goal
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

    def SimulatedAnnealingSearch(self):
        self.reset_stats()
        start_time = time.time()
        start, goal = self.start, self.goal
        cha = {}
        H = start  # trạng thái hiện tại
        self.visited = {H}  # đánh dấu các vị trí đã đi

        self.list_tt_duyet.append(start)
        dosau = 0

        while True:
            row, col = H
            if (row, col) == goal:
                self.duong_di = self.tim_duongdi(start, H, cha)
                self.Dodai_duongdi = len(self.duong_di)
                self.execution_time = time.time() - start_time
                return self.list_tt_duyet, self.duong_di

            T = self.NhietDoT(dosau) # Tính nhiệt độ
            if T < 1e-100:
                break

            queue = self.sinh_tt_con(row, col, self.visited) # Sinh các trạng thái lân cận chưa đi
            self.So_tt_dasinh += len(queue)

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
                self.list_tt_duyet.append(H)
                self.So_tt_daduyet += 1
            dosau += 1  # tăng độ sâu để giảm T

        self.execution_time = time.time() - start_time
        return self.list_tt_duyet, []


