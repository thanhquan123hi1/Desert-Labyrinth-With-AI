import random
import numpy as np
import time

MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]


class NOOBS:
    def __init__(self, matrix, starts, goals):
        self.matrix = np.array(matrix)
        self.rows, self.cols = self.matrix.shape
        self.starts = set(starts)
        self.goals = set(goals)
        self.visited = set()
        self.path = []             # lưu chuỗi belief
        self.execution_time = 0.0  # thời gian chạy

    # ------------------------------------------------------------
    def is_valid(self, x, y):
        return 0 <= x < self.rows and 0 <= y < self.cols and self.matrix[x, y] == 0

    def action(self, belief, move):
        new_belief = set()
        dx, dy = move
        for (x, y) in belief:
            if self.is_valid(x + dx, y + dy):
                new_belief.add((x + dx, y + dy))
            else:
                new_belief.add((x, y))  # nếu đụng tường thì ở lại
        return frozenset(new_belief)

    def is_goal_belief(self, belief):
        return all(state in self.goals for state in belief)

    # ------------------------------------------------------------
    def dfs_belief(self, belief, path):
        """Tìm kiếm theo không gian belief bằng DFS"""
        if belief in self.visited:
            return None
        self.visited.add(belief)

        # Kiểm tra goal
        if self.is_goal_belief(belief):
            return path + [belief]

        for move in MOVES:
            new_belief = self.action(belief, move)
            result = self.dfs_belief(new_belief, path + [belief])
            if result:
                return result
        return None

    def search(self):
        """Chạy toàn bộ thuật toán"""
        start_time = time.time()
        start_belief = frozenset(self.starts)
        self.path = self.dfs_belief(start_belief, []) or []
        self.execution_time = time.time() - start_time
        return self.path

    # ------------------------------------------------------------
    def thong_so(self):
        """Trả về thống kê để hiển thị lên giao diện"""
        return {
            "Số belief duyệt: ": len(self.visited),
            "Độ dài đường đi (belief): ": len(self.path),
            "Thời gian chạy (s): ": round(self.execution_time, 6)
        }


# ======================================================
def find_start_beliefs(matrix, n=3):
    """
    Chọn ngẫu nhiên n ô hợp lệ (giá trị = 0) trong toàn mê cung làm tập belief ban đầu.
    """
    valid_positions = [
        (i, j)
        for i in range(len(matrix))
        for j in range(len(matrix[0]))
        if matrix[i][j] == 0
    ]

    if len(valid_positions) <= n:
        return valid_positions
    return random.sample(valid_positions, n)


def find_goal_beliefs(matrix, n=3):
    goals = []
    for i in range(len(matrix) - 1, -1, -1):
        for j in range(len(matrix[0]) - 1, -1, -1):
            if matrix[i][j] == 0:
                goals.append((i, j))
                if len(goals) == n:
                    return goals
    return goals
