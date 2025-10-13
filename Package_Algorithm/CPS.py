import numpy as np
import time

# 4 hướng di chuyển
DICHUYEN = [(-1, 0), (0, -1), (0, 1), (1, 0)]


class CPS:
    def __init__(self, map_model, start=(1, 1), goal=(19, 28)):
        self.map_model = map_model
        self.maze = np.array(map_model.collision_matrix)
        self.rows, self.cols = self.maze.shape
        self.start = start
        self.goal = goal
        self.reset_stats()

        self.variables = [self.start]
        self.domains = {self.start: self.sinh_mien(self.start)}  # tập giá trị của biến start

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
        for dx, dy in DICHUYEN:
            new_x, new_y = r + dx, c + dy
            domain.append((new_x, new_y))
        np.random.shuffle(domain)
        return domain

    def is_consistent(self, var, value, visited):
        (r2, c2) = value
        if not (0 <= r2 < self.rows and 0 <= c2 < self.cols):
            return False
        if self.maze[r2, c2] == 1:
            return False
        if value in visited:
            return False
        return True

    def run(self):
        self.reset_stats()
        start_time = time.time()
        visited = set()

        result = self.backtrack(self.start, self.goal, visited)
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
            "Số trạng thái đã duyệt: ": self.So_tt_daduyet,
            "Số trạng thái đã sinh: ": self.So_tt_dasinh,
            "Độ dài đường đi: ": self.Dodai_duongdi,
            "Thời gian chạy (s): ": round(self.execution_time, 6),
        }


class Backtracking(CPS):
    def __init__(self, map_model, start=(1, 1), goal=(19, 28)):
        super().__init__(map_model, start, goal)
        self.dead_ends = set()  # bộ nhớ ngõ cụt

    def backtrack(self, cur, goal, visited):
        # Nếu là ngõ cụt đã biết nên bỏ qua
        if cur in self.dead_ends:
            return None

        self.So_tt_daduyet += 1
        self.list_tt_duyet.append(cur)

        if cur == goal:
            return [goal]

        if cur not in self.domains:
            self.domains[cur] = self.sinh_mien(cur)

        valid_values = [v for v in self.domains[cur] if self.is_consistent(cur, v, visited)]
        self.So_tt_dasinh += len(valid_values)

        for value in valid_values:
            visited.add(cur)
            self.variables.append(value)

            result = self.backtrack(value, goal, visited)
            if result is not None:
                return [cur] + result

            visited.remove(cur)
            self.variables.pop()

        # Nếu không tìm thấy đường đánh dấu là ngõ cụt
        self.dead_ends.add(cur)
        return None


class ForwardChecking(CPS):
    def __init__(self, map_model, start=(1, 1), goal=(19, 28)):
        super().__init__(map_model, start, goal)
        self.dead_ends = set()

    def forward_check(self, value, visited):
        for dx, dy in DICHUYEN:
            new_x, new_y = value[0] + dx, value[1] + dy
            ketiep = (new_x, new_y)
            if (0 <= new_x < self.rows and 0 <= new_y < self.cols and
                self.maze[new_x, new_y] == 0 and ketiep not in visited):

                domain = self.sinh_mien(ketiep)
                new_domain = [v for v in domain if self.is_consistent(ketiep, v, visited)]
                if len(new_domain) == 0:
                    return False
        return True

    def backtrack(self, cur, goal, visited):
        if cur in self.dead_ends:
            return None

        self.So_tt_daduyet += 1
        self.list_tt_duyet.append(cur)

        if cur == goal:
            return [goal]

        if cur not in self.domains:
            self.domains[cur] = self.sinh_mien(cur)

        valid_values = [v for v in self.domains[cur] if self.is_consistent(cur, v, visited)]
        self.So_tt_dasinh += len(valid_values)

        for value in valid_values:
            visited.add(cur)
            self.variables.append(value)

            # Bước forward checking
            if self.forward_check(value, visited):
                result = self.backtrack(value, goal, visited)
                if result is not None:
                    return [cur] + result

            visited.remove(cur)
            self.variables.pop()

        self.dead_ends.add(cur)
        return None
