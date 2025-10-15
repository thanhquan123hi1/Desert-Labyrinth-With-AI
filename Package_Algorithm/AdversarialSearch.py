import numpy as np
import random
import time

DICHUYEN = [(0,1),(1,0),(0,-1),(-1,0)]  # phải, xuống, trái, lên

class AdversarialSearch:
    def __init__(self, map_model, start=(1,1), enemy_start=None, goals=None,
                 items=None, traps=None, max_health=3, max_depth=4, recent_limit=4):
        self.map_model = map_model
        self.start = start
        self.enemy_start = enemy_start
        self.goals = goals if goals else []
        self.items = items if items else []
        self.traps = traps if traps else []
        self.max_health = max_health
        self.max_depth = max_depth
        self.recent_limit = recent_limit
        self.reset_stats()

    def reset_stats(self):
        self.list_tt_duyet = []
        self.duong_di_player = []
        self.duong_di_enemy = []
        self.Dodai_duongdi = 0
        self.execution_time = 0
        self.recent_states = []

    def thong_so(self, player_path, enemy_path, state=None):
        # state = (player_pos, enemy_pos, health, collected)
        player_pos = player_path[-1]
        enemy_pos = enemy_path[-1]
        health = state[2] if state else self.max_health
        collected = state[3] if state else set()

        if player_pos == enemy_pos:
            ketqua = "Thua: bị enemy ăn"
        elif health <= 0:
            ketqua = "Thua: mất hết máu"
        elif player_pos in self.goals and len(collected) < len(self.items):
            ketqua = "Thua: đến goal nhưng chưa đủ items"
        else:
            ketqua = "Thắng"

        return {
            "Danh sách trạng thái đã duyệt": self.list_tt_duyet,
            "Độ dài đường đi": self.Dodai_duongdi,
            "Thời gian chạy (s)": round(self.execution_time, 6),
            "Số trạng thái đã duyệt": len(self.list_tt_duyet),
            "Kết quả": ketqua
        }

    def is_valid(self, pos):
        x, y = pos
        return 0 <= x < self.map_model.collision_matrix.shape[0] and \
               0 <= y < self.map_model.collision_matrix.shape[1] and \
               self.map_model.collision_matrix[x, y] != 1

    def hanhdongs(self, pos):
        return [(pos[0]+dx, pos[1]+dy) for dx, dy in DICHUYEN if self.is_valid((pos[0]+dx, pos[1]+dy))]

    def result(self, state, player_action, enemy_action):
        player_pos, enemy_pos, health, collected = state
        next_player = player_action
        next_enemy = enemy_action
        next_health = health
        next_collected = collected.copy()

        if next_player in self.traps:
            next_health -= 1
        if next_player in self.items and next_player not in collected:
            next_collected.add(next_player)

        return (next_player, next_enemy, next_health, next_collected)

    def terminal_test(self, state):
        player_pos, enemy_pos, health, collected = state
        # Bị chết hoặc gặp enemy → kết thúc
        if health <= 0 or player_pos == enemy_pos:
            return True
        # Đạt goal mà đã đủ items → thắng
        if len(collected) == len(self.items) and player_pos in self.goals:
            return True
        # Đến goal nhưng chưa đủ items → xem như nhánh tệ
        if player_pos in self.goals and len(collected) < len(self.items):
            return True
        return False

    def danhgia(self, state):
        player_pos, enemy_pos, health, collected = state
        if health <= 0 or player_pos == enemy_pos:
            return -1000
        if len(collected) == len(self.items) and player_pos in self.goals:
            return 1000

        score = len(collected) * 100

        # Phạt gần bẫy
        for trap in self.traps:
            dist_trap = abs(player_pos[0] - trap[0]) + abs(player_pos[1] - trap[1])
            score -= 200 if dist_trap == 0 else 20 / dist_trap

        # Phạt gần enemy
        dist_enemy = abs(player_pos[0] - enemy_pos[0]) + abs(player_pos[1] - enemy_pos[1])
        score -= 500 if dist_enemy == 0 else 50 / dist_enemy

        # Thưởng gần items còn lại
        remaining_items = [i for i in self.items if i not in collected]
        if remaining_items:
            dists = [abs(player_pos[0]-ix)+abs(player_pos[1]-iy) for ix,iy in remaining_items]
            score -= min(dists)

        # Thưởng đến goal nếu đã đủ items
        if not remaining_items:
            dists_goal = [abs(player_pos[0]-gx)+abs(player_pos[1]-gy) for gx,gy in self.goals]
            score -= min(dists_goal)

        return score

    # -------------- MINIMAX FULL ADVERSARIAL --------------
    def run_minimax(self):
        self.reset_stats()
        start_time = time.time()
        state = (self.start, self.enemy_start, self.max_health, set())
        player_path = [self.start]
        enemy_path = [self.enemy_start]

        while not self.terminal_test(state):
            next_player = self.minimax_decision(state)
            # Enemy đi tất cả hướng → random fallback
            ex, ey = state[1]
            enemy_moves = self.hanhdongs((ex, ey)) or [state[1]]
            next_enemy = random.choice(enemy_moves)
            state = self.result(state, next_player, next_enemy)

            player_path.append(state[0])
            enemy_path.append(state[1])

            self.recent_states.append(state[0])
            if len(self.recent_states) > self.recent_limit:
                self.recent_states.pop(0)

        self.duong_di_player = player_path
        self.duong_di_enemy = enemy_path
        self.Dodai_duongdi = len(player_path)
        self.execution_time = time.time() - start_time
        return player_path, enemy_path

    def minimax_decision(self, state):
        def max_value(state, depth):
            if self.terminal_test(state) or depth == 0:
                return self.danhgia(state)
            v = float('-inf')
            for player_action in self.hanhdongs(state[0]):
                ex, ey = state[1]
                enemy_moves = self.hanhdongs((ex, ey)) or [state[1]]
                for enemy_action in enemy_moves:
                    next_state = self.result(state, player_action, enemy_action)
                    score = min_value(next_state, depth-1)
                    if next_state[0] in self.recent_states:
                        score -= 50
                    v = max(v, score)
            return v

        def min_value(state, depth):
            if self.terminal_test(state) or depth == 0:
                return self.danhgia(state)
            v = float('inf')
            for player_action in self.hanhdongs(state[0]):
                ex, ey = state[1]
                enemy_moves = self.hanhdongs((ex, ey)) or [state[1]]
                for enemy_action in enemy_moves:
                    next_state = self.result(state, player_action, enemy_action)
                    if next_state[0] in self.recent_states:
                        continue
                    v = min(v, max_value(next_state, depth-1))
            return v

        best_score = float('-inf')
        best_action = self.hanhdongs(state[0])[0]
        for player_action in self.hanhdongs(state[0]):
            ex, ey = state[1]
            enemy_moves = self.hanhdongs((ex, ey)) or [state[1]]
            min_scores = []
            for enemy_action in enemy_moves:
                next_state = self.result(state, player_action, enemy_action)
                if next_state[0] in self.recent_states:
                    continue
                min_scores.append(min_value(next_state, self.max_depth-1))
            if min_scores:
                score = min(min_scores)
                if score > best_score:
                    best_score = score
                    best_action = player_action
        return best_action

    # -------------- ALPHA-BETA FULL ADVERSARIAL --------------
    def run_alphabeta(self):
        self.reset_stats()
        start_time = time.time()
        state = (self.start, self.enemy_start, self.max_health, set())
        player_path = [self.start]
        enemy_path = [self.enemy_start]

        while not self.terminal_test(state):
            next_player = self.alpha_beta_decision(state)
            ex, ey = state[1]
            enemy_moves = self.hanhdongs((ex, ey)) or [state[1]]
            next_enemy = random.choice(enemy_moves)
            state = self.result(state, next_player, next_enemy)

            player_path.append(state[0])
            enemy_path.append(state[1])

            self.recent_states.append(state[0])
            if len(self.recent_states) > self.recent_limit:
                self.recent_states.pop(0)

        self.duong_di_player = player_path
        self.duong_di_enemy = enemy_path
        self.Dodai_duongdi = len(player_path)
        self.execution_time = time.time() - start_time
        return player_path, enemy_path

    def alpha_beta_decision(self, state):
        def max_value(state, alpha, beta, depth):
            if self.terminal_test(state) or depth == 0:
                return self.danhgia(state)
            v = float('-inf')
            for player_action in self.hanhdongs(state[0]):
                ex, ey = state[1]
                enemy_moves = self.hanhdongs((ex, ey)) or [state[1]]
                for enemy_action in enemy_moves:
                    next_state = self.result(state, player_action, enemy_action)
                    score = min_value(next_state, alpha, beta, depth-1)
                    if next_state[0] in self.recent_states:
                        score -= 50
                    v = max(v, score)
                    if v >= beta:
                        return v
                    alpha = max(alpha, v)
            return v

        def min_value(state, alpha, beta, depth):
            if self.terminal_test(state) or depth == 0:
                return self.danhgia(state)
            v = float('inf')
            for player_action in self.hanhdongs(state[0]):
                ex, ey = state[1]
                enemy_moves = self.hanhdongs((ex, ey)) or [state[1]]
                for enemy_action in enemy_moves:
                    next_state = self.result(state, player_action, enemy_action)
                    if next_state[0] in self.recent_states:
                        continue
                    v = min(v, max_value(next_state, alpha, beta, depth-1))
                    if v <= alpha:
                        return v
                    beta = min(beta, v)
            return v

        best_score = float('-inf')
        best_action = self.hanhdongs(state[0])[0]
        alpha = float('-inf')
        beta = float('inf')
        for player_action in self.hanhdongs(state[0]):
            ex, ey = state[1]
            enemy_moves = self.hanhdongs((ex, ey)) or [state[1]]
            min_scores = []
            for enemy_action in enemy_moves:
                next_state = self.result(state, player_action, enemy_action)
                if next_state[0] in self.recent_states:
                    continue
                min_scores.append(min_value(next_state, alpha, beta, self.max_depth-1))
            if min_scores:
                score = min(min_scores)
                if score > best_score:
                    best_score = score
                    best_action = player_action
            alpha = max(alpha, best_score)
        return best_action

# ---------------- Test chạy ----------------
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

if __name__ == "__main__":
    map_model = MapModel()
    search = AdversarialSearch(map_model,
        start=(1,1),
        enemy_start=(18, 28),
        goals=[(1, 27), (19, 28), (19, 1)],
        items=[(5, 2), (5, 4), (11, 10)],
        traps=[(3, 4), (7, 7), (15, 15)],
        max_health=3,
        max_depth=4
    )

    print("=== Minimax full adversarial ===")
    player_path, enemy_path = search.run_minimax()
    print("Đường đi Player :", player_path)
    print("Đường đi Enemy  :", enemy_path)
    print("Thống kê:", search.thong_so(player_path, enemy_path))

    print("\n=== Alpha-Beta full adversarial ===")
    player_path, enemy_path = search.run_alphabeta()
    print("Đường đi Player :", player_path)
    print("Đường đi Enemy  :", enemy_path)
    print("Thống kê:", search.thong_so(player_path, enemy_path))
