import numpy as np
import time


# 4 hướng di chuyển
DICHUYEN = [(-1, 0), (0, -1), (0, 1), (1, 0)]


class Backtracking:
    def __init__(self, map_model, start=(1, 1), goal=(19, 28)):
        self.map_model = map_model
        self.maze = np.array(map_model.collision_matrix)
        self.rows, self.cols = self.maze.shape
        self.start = start
        self.goal = goal
        self.reset_stats()

        self.variables = [self.start]       
        self.domains = {self.start: self.sinh_mien(self.start)}  # domain của start

    # ---------------------------------------------------------------------
    def reset_stats(self):
        self.list_tt_duyet = []
        self.duong_di = []
        self.So_tt_daduyet = 0
        self.So_tt_dasinh = 0
        self.Dodai_duongdi = 0
        self.execution_time = 0

    def sinh_mien(self, var):
        (r, c) = var
        domain = []
        for dr, dc in DICHUYEN:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self.maze[nr, nc] != 1:
                    domain.append((nr, nc))
        np.random.shuffle(domain) # random để có giá trị ngẫu nhiên cho biến
        return domain

    # ---------------------------------------------------------------------
    def is_consistent(self, var, value, assignment):
        # Không ra khỏi mê cung
        (r2, c2) = value
        if not (0 <= r2 < self.rows and 0 <= c2 < self.cols):
            return False

        # Không đi vào tường
        if self.maze[r2, c2] == 1:
            return False

        # Phải liền kề
        (r1, c1) = var
        if abs(r1 - r2) + abs(c1 - c2) != 1:
            return False

        # Không quay lại trạng thái đã đi
        if value in assignment:
            return False

        return True
    
    # xử lý đệ quy
    def backtrack(self, current, goal, assignment):
        self.So_tt_daduyet += 1
        self.list_tt_duyet.append(current)

        # Nếu đã đến goal
        if current == goal:
            return [goal]

        # Nếu current chưa có miền giá trị thì sinh domain mới
        if current not in self.domains:
            self.domains[current] = self.sinh_mien(current)

        # Duyệt tất cả giá trị khả dĩ
        for value in self.domains[current]:
            if self.is_consistent(current, value, assignment):
                # Gán biến current -> value
                assignment[current] = value
                self.So_tt_dasinh += 1
                self.variables.append(value)

                # Đệ quy tới bước kế tiếp
                result = self.backtrack(value, goal, assignment)
                if result is not None:
                    return [current] + result

                # Nếu thất bại, quay lui
                del assignment[current]
                self.variables.pop()

        return None

    # hàm này để gọi trong module algorithm_manager.py
    def Backtracking(self):
        self.reset_stats()
        start_time = time.time()
        assignment = {}

        result = self.backtrack(self.start, self.goal, assignment)
        self.execution_time = time.time() - start_time

        if result:
            self.duong_di = result
            self.Dodai_duongdi = len(result)
        else:
            self.duong_di = []

        return self.list_tt_duyet, self.duong_di

    def thong_so(self):
        success = len(self.duong_di) > 0
        return {
            "Kết quả": "Thành công" if success else "Thất bại",
            "Số trạng thái đã duyệt": self.So_tt_daduyet,
            "Số trạng thái đã sinh": self.So_tt_dasinh,
            "Độ dài đường đi": self.Dodai_duongdi,
            "Thời gian chạy (s)": round(self.execution_time, 6),
        }
