import numpy as np
import time

DICHUYEN = [(0,1),(1,0),(0,-1),(-1,0)]

class CES_AndOrSearch:
    def __init__(self, map_model, start=(1, 1), goal=(19, 28)):
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
    #-------Chạy thuật toán AndOrSearch-------
    # Hành động thực hiện lên người chơi
    def move(self, state):
        x, y = state
        actions = []
        for dx, dy in DICHUYEN:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.num_rows and 0 <= ny < self.num_cols:
                if self.tt_bandau[nx, ny] != 1 and (nx, ny) not in self.list_tt_duyet:
                    actions.append((nx, ny))
        return actions

    # OR node: chọn 1 hành động
    def or_search(self, state, path, cha):
        if state in path:
            return None  # fail nếu đã đi qua state

        self.list_tt_duyet.append(state)
        self.So_tt_daduyet += 1

        if state == self.goal:
            return [state]

        for next_state in self.move(state):
            self.So_tt_dasinh += 1
            # Gọi AND node (nhưng trong maze cổ điển AND node chỉ gọi OR node trở lại)
            subplan = self.and_search([next_state], path + [state], cha)
            if subplan is not None:
                cha[next_state] = state
                return [state] + subplan

        return None

    # AND node (chỉ ghi đủ hình thức, không sinh nhánh non-deterministic)
    def and_search(self, states, path, cha):
        plans = []
        for s in states:
            subplan = self.or_search(s, path, cha)
            if subplan is None:
                return None  # fail nếu 1 state fail
            plans.extend(subplan)
        return plans

    def AndOrSearch(self):
        start_time = time.time()
        cha = {}
        plan = self.or_search(self.start, [], cha)
        if plan:
            self.duong_di = plan
            self.Dodai_duongdi = len(plan)
        self.execution_time = time.time() - start_time
        return self.list_tt_duyet, self.duong_di


