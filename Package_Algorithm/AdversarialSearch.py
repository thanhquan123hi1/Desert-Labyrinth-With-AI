import time
from collections import deque
import numpy as np
import os

# 4 hướng: lên, trái, phải, xuống
DICHUYEN = [(-1, 0), (0, -1), (0, 1), (1, 0)]

class AdversarialSearch:
    """
    Minimax & Alpha-Beta áp dụng cho mê cung rượt đuổi.
    - MAX = Player: cố gắng đến goal và tránh bị bắt
    - MIN = Enemy: cố gắng bắt player / cản đường
    """
    def __init__(self, map_model, start=(1, 1), enemy_start=None, goals=None,
                 max_depth=8, step_limit=300, allow_stay=False):
        self.map_model = map_model
        self.start = start
        self.enemy_start = enemy_start
        self.goals = list(goals) if goals else []
        self.max_depth = int(max_depth)
        self.step_limit = int(step_limit)
        self.allow_stay = bool(allow_stay)
        self.rows, self.cols = map_model.collision_matrix.shape
        self.last_run_algorithm = None
        self.reset_stats()

    def reset_stats(self):
        self.execution_time = 0.0
        self.duong_di_player = []
        self.duong_di_enemy = []
        self.last_run_algorithm = None

    def thong_so(self):
        result = "Thua"
        if self.duong_di_player:
            player_pos_end = self.duong_di_player[-1]
            enemy_pos_end = self.duong_di_enemy[-1]
            if player_pos_end in self.goals and player_pos_end != enemy_pos_end:
                result = "Thắng"
        return {
            "Thuật toán": self.last_run_algorithm,
            "Kết quả": result,
            "Độ dài đường đi Player": len(self.duong_di_player) - 1 if self.duong_di_player else 0,
            "Độ dài đường đi Enemy": len(self.duong_di_enemy) - 1 if self.duong_di_enemy else 0,
            "Thời gian chạy (s)": round(self.execution_time, 6),
        }

    def _is_free(self, r, c):
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.map_model.collision_matrix[r, c] != 1
        return False

    def _neighbors(self, pos):
        r, c = pos
        moves = []
        for dr, dc in DICHUYEN:
            r1, c1 = r + dr, c + dc
            if self._is_free(r1, c1):
                moves.append((r1, c1))
        if self.allow_stay:
            moves.append(pos)
        return moves

    def _bfs_distance(self, src, targets):
        if not targets: return 10**6
        if src in targets: return 0
        q = deque([src])
        dist = {src: 0}
        while q:
            r, c = q.popleft()
            d = dist[(r, c)]
            for (r1, c1) in self._neighbors((r, c)):
                if (r1, c1) not in dist:
                    dist[(r1, c1)] = d + 1
                    if (r1, c1) in targets:
                        return d + 1
                    q.append((r1, c1))
        return 10**6

    def _evaluate(self, player, enemy):
        if player == enemy: return -1_000_000
        if player in self.goals: return +1_000_000
        d_goal = self._bfs_distance(player, set(self.goals))
        d_enemy = self._bfs_distance(player, {enemy})
        unreachable_penalty = 2_000 if d_goal >= 10**6 else 0
        w_goal = 200.0
        w_safe = 30.0
        return -w_goal * d_goal + w_safe * d_enemy - unreachable_penalty

    def run_minimax(self):
        self.reset_stats()
        self.last_run_algorithm = "Minimax"
        t0 = time.time()
        player, enemy = self.start, self.enemy_start
        path_p, path_e = [player], [enemy]
        steps = 0
        while steps < self.step_limit and player != enemy and player not in self.goals:
            player_next = self._minimax_decision(player, enemy)
            enemy_next = self._minimizer_best_reply(player_next, enemy, use_alpha_beta=False)
            player, enemy = player_next, enemy_next
            path_p.append(player)
            path_e.append(enemy)
            steps += 1
        self.duong_di_player = path_p
        self.duong_di_enemy = path_e
        self.execution_time = time.time() - t0
        return path_p, path_e

    def _minimax_decision(self, player, enemy):
        def max_value(pl, en, depth):
            if depth == 0 or pl == en or pl in self.goals: return self._evaluate(pl, en)
            v = float("-inf")
            for a in self._neighbors(pl):
                v = max(v, min_value(a, en, depth - 1))
            return v
        def min_value(pl, en, depth):
            if depth == 0 or pl == en or pl in self.goals: return self._evaluate(pl, en)
            v = float("inf")
            for b in self._neighbors(en):
                v = min(v, max_value(pl, b, depth - 1))
            return v
        best_score = float("-inf")
        best_action = player
        for a in self._neighbors(player):
            score = min_value(a, enemy, self.max_depth - 1)
            if score > best_score:
                best_score = score
                best_action = a
        return best_action

    def _minimizer_best_reply(self, player_after, enemy_now, use_alpha_beta=False):
        if not use_alpha_beta:
            def max_value(pl, en, depth):
                if depth == 0 or pl == en or pl in self.goals: return self._evaluate(pl, en)
                v = float("-inf")
                for a in self._neighbors(pl): v = max(v, min_value(a, en, depth - 1))
                return v
            def min_value(pl, en, depth):
                if depth == 0 or pl == en or pl in self.goals: return self._evaluate(pl, en)
                v = float("inf")
                for b in self._neighbors(en): v = min(v, max_value(pl, b, depth - 1))
                return v
            best_v = float("inf")
            best_b = enemy_now
            for b in self._neighbors(enemy_now):
                v = max_value(player_after, b, self.max_depth - 1)
                if v < best_v:
                    best_v, best_b = v, b
            return best_b
        else:
            def max_value(pl, en, depth, alpha, beta):
                if depth == 0 or pl == en or pl in self.goals: return self._evaluate(pl, en)
                v = float("-inf")
                for a in self._neighbors(pl):
                    v = max(v, min_value(a, en, depth - 1, alpha, beta))
                    if v >= beta: return v
                    alpha = max(alpha, v)
                return v
            def min_value(pl, en, depth, alpha, beta):
                if depth == 0 or pl == en or pl in self.goals: return self._evaluate(pl, en)
                v = float("inf")
                for b in self._neighbors(en):
                    v = min(v, max_value(pl, b, depth - 1, alpha, beta))
                    if v <= alpha: return v
                    beta = min(beta, v)
                return v
            best_v = float("inf")
            best_b = enemy_now
            alpha, beta = float("-inf"), float("inf")
            for b in self._neighbors(enemy_now):
                v = max_value(player_after, b, self.max_depth - 1, alpha, beta)
                if v < best_v:
                    best_v, best_b = v, b
                beta = min(beta, best_v)
            return best_b

    def run_alphabeta(self):
        self.reset_stats()
        self.last_run_algorithm = "Alpha-Beta"
        t0 = time.time()
        player, enemy = self.start, self.enemy_start
        path_p, path_e = [player], [enemy]
        steps = 0
        while steps < self.step_limit and player != enemy and player not in self.goals:
            player_next = self._alphabeta_decision(player, enemy)
            enemy_next = self._minimizer_best_reply(player_next, enemy, use_alpha_beta=True)
            player, enemy = player_next, enemy_next
            path_p.append(player)
            path_e.append(enemy)
            steps += 1
        self.duong_di_player = path_p
        self.duong_di_enemy = path_e
        self.execution_time = time.time() - t0
        return path_p, path_e

    def _alphabeta_decision(self, player, enemy):
        def max_value(pl, en, depth, alpha, beta):
            if depth == 0 or pl == en or pl in self.goals: return self._evaluate(pl, en)
            v = float("-inf")
            for a in self._neighbors(pl):
                v = max(v, min_value(a, en, depth - 1, alpha, beta))
                if v >= beta: return v
                alpha = max(alpha, v)
            return v
        def min_value(pl, en, depth, alpha, beta):
            if depth == 0 or pl == en or pl in self.goals: return self._evaluate(pl, en)
            v = float("inf")
            for b in self._neighbors(en):
                v = min(v, max_value(pl, b, depth - 1, alpha, beta))
                if v <= alpha: return v
                beta = min(beta, v)
            return v
        best_score = float("-inf")
        best_action = player
        alpha, beta = float("-inf"), float("inf")
        for a in self._neighbors(player):
            score = min_value(a, enemy, self.max_depth - 1, alpha, beta)
            if score > best_score:
                best_score = score
                best_action = a
            alpha = max(alpha, best_score)
        return best_action

