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

    # Tạo tập giá trị khả dĩ cho một biến
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
        (r1, c1) = var
        if abs(r1 - r2) + abs(c1 - c2) != 1:
            return False
        if value in visited:
            return False
        return True

    # Chạy thuật toán (chung)
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


# ======================================================================
#                           BACKTRACKING
# ======================================================================
class Backtracking(CPS):
    def backtrack(self, cur, goal, visited):
        self.So_tt_daduyet += 1                     # 🔹 mỗi khi mở rộng 1 node
        self.list_tt_duyet.append(cur)

        if cur == goal:
            return [goal]

        if cur not in self.domains:
            self.domains[cur] = self.sinh_mien(cur)

        # Sinh ra các giá trị hợp lệ
        valid_values = [v for v in self.domains[cur] if self.is_consistent(cur, v, visited)]
        self.So_tt_dasinh += len(valid_values)      # ✅ tổng số con hợp lệ được sinh ra

        for value in valid_values:
            visited.add(cur)
            self.variables.append(value)

            result = self.backtrack(value, goal, visited)
            if result is not None:
                return [cur] + result

            visited.remove(cur)
            self.variables.pop()

        return None


# ======================================================================
#                           FORWARD CHECKING
# ======================================================================
class ForwardChecking(CPS):
    def forward_check(self, value, visited):
        """Kiểm tra ràng buộc cho bước kế tiếp"""
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
        self.So_tt_daduyet += 1
        self.list_tt_duyet.append(cur)

        if cur == goal:
            return [goal]

        if cur not in self.domains:
            self.domains[cur] = self.sinh_mien(cur)

        # Sinh trước tất cả giá trị hợp lệ
        valid_values = [v for v in self.domains[cur] if self.is_consistent(cur, v, visited)]
        self.So_tt_dasinh += len(valid_values)      # ✅ tổng số con hợp lệ được sinh ra

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
        return None
