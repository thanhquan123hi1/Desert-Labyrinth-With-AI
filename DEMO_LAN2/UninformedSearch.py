import numpy as np
import time
from collections import deque
import random

DICHUYEN = [(0,1),(1,0),(0,-1),(-1,0)] # phải, xuống, trái, lên

class UninformedSearch:
    def __init__(self, map_model, start=(1,1), enemy_start=None, goals=None,
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
            "Thời gian chạy (s)": round(self.execution_time,6)
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
            if enemy_moves:#Tính k/c Mahattan từ ô tới Player-->Chọn tất cả các ô có k/c nhỏ nhất-->Random chọn 1
                distances = [abs(px - nx) + abs(py - ny) for nx, ny in enemy_moves]
                min_dist = min(distances)
                best_moves = [pos for pos, dist in zip(enemy_moves, distances) if dist == min_dist]
                next_enemy = random.choice(best_moves)
            else:
                next_enemy = (ex, ey)

            children.append((next_player, next_enemy, next_health))

        return children

    # BFS cho nhiều mục tiêu
    def search_multiple_goals(self, method="BFS"):
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
            if method == "DFS":
                path_player, path_enemy, health = self.DFS(player_pos, enemy_pos, goals, current_health)
            else:
                path_player, path_enemy, health = self.BFS(player_pos, enemy_pos, goals, current_health)

            if not path_player:
                print(f"Không tìm được đường tới item (còn lại: {remaining_items})")
                return total_path_player, total_path_enemy

            found_item = path_player[-1]
            if found_item in remaining_items:
                remaining_items.remove(found_item)

            total_path_player.extend(path_player)
            total_path_enemy.extend(path_enemy)

            player_pos, enemy_pos = path_player[-1], path_enemy[-1]
            current_health = health # cập nhật máu theo đường đi vừa đi

        # Đi tới goal cuối cùng
        goals = self.goals
        if method == "DFS":
            path_player, path_enemy, health = self.DFS(player_pos, enemy_pos, goals,  current_health)
        else:
            path_player, path_enemy, health = self.BFS(player_pos, enemy_pos, goals,  current_health)

        if not path_player:
            print(f"Không tìm được đường tới Goal")
            return total_path_player, total_path_enemy

        total_path_player.extend(path_player)
        total_path_enemy.extend(path_enemy)

        self.duong_di_player = total_path_player
        self.duong_di_enemy = total_path_enemy
        self.Dodai_duongdi = len(total_path_player)
        self.execution_time = time.time() - start_time
        return total_path_player, total_path_enemy

    #------Thuật toán BFS------
    def BFS(self, start_player, start_enemy, goals, health):
        queue = deque([((start_player, start_enemy, health), [], [])])
        visited = set()
        visited.add(start_player)

        temp_path_p = []  # lưu tạm đường đi nếu bị bắt
        temp_path_e = []

        while queue:
            (player_pos, enemy_pos, health), path_player, path_enemy = queue.popleft()

            self.list_tt_duyet.append(player_pos)
            self.So_tt_daduyet += 1

            if player_pos in goals:
                return path_player + [player_pos], path_enemy + [enemy_pos], health

            for child in self.sinh_tt_con(player_pos, enemy_pos, health):
                next_player, next_enemy, next_health = child

                if next_player == next_enemy:
                    temp_path_p = path_player + [player_pos, next_player]
                    temp_path_e = path_enemy + [enemy_pos, next_enemy]
                    continue

                key = next_player  # kiểm tra vị trí Player + items
                if key not in visited:
                    visited.add(key)
                    self.So_tt_dasinh += 1
                    queue.append((child, path_player + [player_pos], path_enemy + [next_enemy]))

        return temp_path_p, temp_path_e, health

    # ------Thuật toán DFS------
    def DFS(self, start_player, start_enemy, goals, health):
        stack = [((start_player, start_enemy, health), [], [])]
        visited = set()
        visited.add(start_player)

        temp_path_p = []  # lưu tạm đường đi nếu bị bắt
        temp_path_e = []

        while stack:
            (player_pos, enemy_pos, health), path_player, path_enemy = stack.pop()
            self.list_tt_duyet.append(player_pos)
            self.So_tt_daduyet += 1

            if player_pos in goals:
                return path_player + [player_pos], path_enemy + [enemy_pos], health

            for child in self.sinh_tt_con(player_pos, enemy_pos, health):
                next_player, next_enemy, next_health = child

                if next_player == next_enemy:
                    temp_path_p = path_player + [player_pos, next_player]
                    temp_path_e = path_enemy + [enemy_pos, next_enemy]
                    continue

                key = next_player # kiểm tra Player + items
                if key not in visited:
                    visited.add(key)
                    self.So_tt_dasinh += 1
                    stack.append((child, path_player + [player_pos], path_enemy + [next_enemy]))

        return temp_path_p, temp_path_e, health


# Test
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
search = UninformedSearch(
    map_model,
    start=(1, 1),
    enemy_start=(18, 28),
    goals=[(1, 27), (19, 28), (19, 1)],
    items=[(5, 2), (5, 4), (11, 10)],
    traps=[(3, 4), (7, 7), (15, 15)],
    max_health=3)
player_path, enemy_path = search.search_multiple_goals(method="BFS")
print("=== BFS ===")
print("Đường đi Player:", player_path)
print("Đường đi Enemy:", enemy_path)
print("Thống kê:", search.thong_so())
player_path, enemy_path = search.search_multiple_goals(method="DFS")
print("=== DFS ===")
print("Đường đi Player:", player_path)
print("Đường đi Enemy:", enemy_path)
print("Thống kê:", search.thong_so())