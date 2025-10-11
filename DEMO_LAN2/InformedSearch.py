import heapq
import numpy as np
import time
import random

DICHUYEN = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # phải, xuống, trái, lên

class InformedSearch:
    def __init__(self, map_model, start=(1, 1), enemy_start=None, goals=None,
                 items=None, traps=None, max_health=3):
        self.map_model = map_model
        self.num_rows, self.num_cols = map_model.collision_matrix.shape
        self.start = start
        self.enemy_start = enemy_start
        self.goals = goals if goals else []
        self.items = items if items else []
        self.traps = traps if traps else []
        self.max_health = max_health
        self.reset_stats()

    def reset_stats(self):
        self.list_tt_duyet = []
        self.duong_di_player = []
        self.duong_di_enemy = []
        self.So_tt_daduyet = 0
        self.So_tt_dasinh = 0
        self.Dodai_duongdi = 0
        self.execution_time = 0

    def thong_so(self):
        return {
            "Số trạng thái đã duyệt": self.So_tt_daduyet,
            "Danh sách trạng thái đã duyệt": self.list_tt_duyet,
            "Số trạng thái đã sinh": self.So_tt_dasinh,
            "Độ dài đường đi": self.Dodai_duongdi,
            "Thời gian chạy (s)": round(self.execution_time, 6)
        }

    def is_valid(self, pos):
        x, y = pos
        return 0 <= x < self.num_rows and 0 <= y < self.num_cols and self.map_model.collision_matrix[x, y] != 1

    def sinh_tt_con(self, player_pos, enemy_pos, health):
        children = []
        px, py = player_pos
        ex, ey = enemy_pos

        for dx, dy in DICHUYEN:
            next_player = (px + dx, py + dy)
            if not self.is_valid(next_player):
                continue

            next_health = health
            if next_player in self.traps:
                next_health -= 1
                if next_health <= 0:
                    continue

            enemy_moves = [(ex + dx2, ey + dy2) for dx2, dy2 in DICHUYEN if self.is_valid((ex + dx2, ey + dy2))]
            random.seed(5)
            if enemy_moves:
                distances = [abs(px - nx) + abs(py - ny) for nx, ny in enemy_moves]
                min_dist = min(distances)
                best_moves = [pos for pos, dist in zip(enemy_moves, distances) if dist == min_dist]
                next_enemy = random.choice(best_moves)
            else:
                next_enemy = (ex, ey)

            children.append((next_player, next_enemy, next_health))

        return children

    #Hàm Heuristic theo Manhattan + lookedhead_penalty + Dead-end_penalty
    def lookahead_penalty(self, row, col, depth, visited=None, weight=1.0):
        visited = visited or set()
        if depth == 0:
            return 0

        visited.add((row, col))
        moves = []
        for dr, dc in DICHUYEN:
            r1, c1 = row + dr, col + dc
            if 0 <= r1 < self.num_rows and 0 <= c1 < self.num_cols:
                if self.map_model.collision_matrix[r1, c1] != 1 and (r1, c1) not in visited:
                    moves.append((r1, c1))

        if len(moves) == 0: # penalty theo số hướng có thể đi
            penalty = 10 * weight
        elif len(moves) == 1:
            penalty = 1 * weight
        else:
            penalty = 0

        if moves:# Đệ quy lookahead
            next_penalties = [self.lookahead_penalty(r1, c1, depth - 1, visited.copy(), weight * 0.6) for r1, c1 in moves]
            penalty += max(next_penalties)
        return penalty

    def heuristic(self, pos, goals, lookahead_steps=3):
        px, py = pos

        #Manhattan
        goal = min(goals, key=lambda g: abs(px - g[0]) + abs(py - g[1]))
        manhattan = abs(px - goal[0]) + abs(py - goal[1])

        # Dead-end penalty
        moves_now = sum(1 for dr, dc in DICHUYEN
                        if 0 <= px + dr < self.num_rows and 0 <= py + dc < self.num_cols
                        and self.map_model.collision_matrix[px + dr, py + dc] != 1)
        if moves_now == 0:
            dead_end_penalty = 10
        elif moves_now == 1:
            dead_end_penalty = 1
        else:
            dead_end_penalty = 0

        # Lookahead penalty
        lookahead_pen = self.lookahead_penalty(px, py, lookahead_steps)

        return manhattan + dead_end_penalty + lookahead_pen

    # Hàm fx = gx +hx
    def fx(self, g, h):
        return g + h

    def search_multiple_goals(self, method="AStar"):
        self.reset_stats()
        start_time = time.time()

        player_pos = self.start
        enemy_pos = self.enemy_start
        current_health = self.max_health
        total_path_player = []
        total_path_enemy = []

        remaining_items = list(self.items)
        while remaining_items:  # Lần lượt tới từng item còn lại
            goals = remaining_items
            if method == "Greedy":
                path_player, path_enemy, health = self.Greedy(player_pos, enemy_pos, goals, current_health)
            else:
                path_player, path_enemy, health = self.Astar(player_pos, enemy_pos, goals, current_health)

            if not path_player or path_player[-1] == path_enemy[-1]:
                print(f"Không tìm thấy đường tới item (còn lại: {remaining_items})")
                total_path_player.extend(path_player)
                total_path_enemy.extend(path_enemy)
                return total_path_player, total_path_enemy

            found_item = path_player[-1]
            if found_item in remaining_items:
                remaining_items.remove(found_item)

            total_path_player.extend(path_player)
            total_path_enemy.extend(path_enemy)

            player_pos, enemy_pos = path_player[-1], path_enemy[-1]
            current_health = health

        # Đi tới goal cuối
        goals = self.goals
        if method == "Greedy":
            path_player, path_enemy, health = self.Greedy(player_pos, enemy_pos, goals, current_health)
        else:
            path_player, path_enemy, health = self.Astar(player_pos, enemy_pos, goals, current_health)

        if not path_player or path_player[-1] == path_enemy[-1]:
            total_path_player.extend(path_player)
            total_path_enemy.extend(path_enemy)
            return total_path_player, total_path_enemy

        total_path_player.extend(path_player)
        total_path_enemy.extend(path_enemy)

        self.duong_di_player = total_path_player
        self.duong_di_enemy = total_path_enemy
        self.Dodai_duongdi = len(total_path_player)
        self.execution_time = time.time() - start_time
        return total_path_player, total_path_enemy

    # ----Thuật toán Greedy ----
    def Greedy(self, start_player, start_enemy, goals, health):
        priority_queue = []
        visited = set()
        start_state = (start_player, start_enemy, health)

        heapq.heappush(priority_queue, (self.heuristic(start_player, goals), start_state, [], []))
        visited.add(start_player)
        self.So_tt_dasinh += 1

        temp_path_p = []  # lưu tạm đường đi nếu bị bắt
        temp_path_e = []

        while priority_queue:
            _, (player_pos, enemy_pos, health), path_p, path_e = heapq.heappop(priority_queue)
            self.list_tt_duyet.append(player_pos)
            self.So_tt_daduyet += 1

            if player_pos in goals:
                return path_p + [player_pos], path_e + [enemy_pos], health

            for child in self.sinh_tt_con(player_pos, enemy_pos, health):
                next_player, next_enemy, next_health = child

                if next_player == next_enemy:
                    temp_path_p = path_p + [player_pos, next_player]
                    temp_path_e = path_e + [enemy_pos, next_enemy]

                    continue
                if next_player in visited:
                    continue
                visited.add(next_player)
                self.So_tt_dasinh += 1

                h = self.heuristic(next_player, goals)
                heapq.heappush(priority_queue, (h, child, path_p + [player_pos], path_e + [next_enemy]))

        return temp_path_p, temp_path_e, health

    # ----Thuật toán A* ----
    def Astar(self, start_player, start_enemy, goals, health):
        priority_queue = []
        visited = set()
        g_cost = {start_player: 0}

        start_state = (start_player, start_enemy, health)
        heapq.heappush(priority_queue, (self.heuristic(start_player, goals), start_state, [], []))
        visited.add(start_player)
        self.So_tt_dasinh += 1

        temp_path_p = []  # lưu tạm đường đi nếu bị bắt
        temp_path_e = []

        while priority_queue:
            _, (player_pos, enemy_pos, health), path_p, path_e = heapq.heappop(priority_queue)
            self.list_tt_duyet.append(player_pos)
            self.So_tt_daduyet += 1

            if player_pos in goals:
                return path_p + [player_pos], path_e + [enemy_pos], health

            for child in self.sinh_tt_con(player_pos, enemy_pos, health):
                next_player, next_enemy, next_health = child

                if next_player == next_enemy:
                    temp_path_p = path_p + [player_pos, next_player]
                    temp_path_e = path_e + [enemy_pos, next_enemy]
                    continue

                if next_player in visited:
                    continue
                visited.add(next_player)
                self.So_tt_dasinh += 1

                g_new = g_cost[player_pos] + 1
                g_cost[next_player] = g_new
                h = self.heuristic(next_player, goals)
                f = self.fx(g_new, h)

                heapq.heappush(priority_queue, (f, child, path_p + [player_pos], path_e + [next_enemy]))

        return temp_path_p, temp_path_e, health

#TEST
class MapModel:
    def __init__(self):
        self.collision_matrix = np.array([
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
])
        self.num_rows, self.num_cols = self.collision_matrix.shape
map_model = MapModel()
search = InformedSearch(
    map_model,
    start=(1,1),
    enemy_start=(18, 28),
    goals=[(19, 28)],
    items=[(5, 2), (5, 4), (11, 10)], # [(1, 27), (19, 28), (19, 1)] cái này ra kq
    traps=[(3, 4), (7, 7), (15, 15)],
    max_health=3)
player_path, enemy_path = search.search_multiple_goals(method="AStar")
print("=== A* ===")
print("Đường đi Player:", player_path)
print("Đường đi Enemy:", enemy_path)
print("Thống kê:", search.thong_so())
player_path, enemy_path = search.search_multiple_goals(method="Greedy")
print("\n=== Greedy ===")
print("Đường đi Player:", player_path)
print("Đường đi Enemy:", enemy_path)
print("Thống kê:", search.thong_so())
