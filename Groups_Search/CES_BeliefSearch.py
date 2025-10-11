import numpy as np
import time


DICHUYEN = [(0,1),(1,0),(0,-1),(-1,0)]
#tối đa 4 state cho starts
class CES_BeliefSearch:
    def __init__(self, map_model, starts=None, goals=None):

        self.map_model = map_model
        self.tt_bandau = np.array(map_model.collision_matrix)
        self.num_rows, self.num_cols = self.tt_bandau.shape

        self.starts = starts
        self.goals = goals
        self.starts_size = len(starts)
        self.goals_size = len(goals)

        self.reset_stats()

    def reset_stats(self):
        # Lưu riêng list_tt_duyet và duong_di cho từng trạng thái (theo số starts)
        self.list_tt_duyet_belief = [[] for _ in range(self.starts_size)]
        self.duong_di_belief = [[] for _ in range(self.starts_size)]
        self.visited_belief = [set() for _ in range(self.starts_size)]

        # thống kê theo từng start
        self.So_tt_daduyet = [0 for _ in range(self.starts_size)]
        self.So_tt_dasinh = [0 for _ in range(self.starts_size)]
        self.Dodai_duongdi = [0 for _ in range(self.starts_size)]
        self.execution_time = 0


    def thong_so(self):
        return {
            "Số trạng thái đã duyệt: ": self.So_tt_daduyet,
            "Số trạng thái đã sinh: ": self.So_tt_dasinh,
            "Độ dài đường đi: ": self.Dodai_duongdi,
            "Thời gian chạy (s): ": round(self.execution_time, 6)
        }
    def tim_duongdi(self, start, goal, cha):
        path = []
        cur = goal
        while cur != start:
            path.append(cur)
            cur = cha[cur]
        path.append(start)
        path.reverse()
        return path

    # -------Chạy thuật toán BeliefSearch-------
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
        # row, col = vitri
        #
        # # Nếu có nhiều goal, chọn goal gần nhất
        # goals = self.goals
        # manhattan = min(abs(row - g[0]) + abs(col - g[1]) for g in goals)
        #
        # # Dead-end penalty
        # moves_now = sum(1 for dr, dc in DICHUYEN
        #                 if 0 <= row + dr < self.num_rows and 0 <= col + dc < self.num_cols
        #                 and self.tt_bandau[row + dr, col + dc] != 1)
        #
        # if moves_now == 0:
        #     dead_end_penalty = 10
        # elif moves_now == 1:
        #     dead_end_penalty = 1
        # else:
        #     dead_end_penalty = 0
        #
        # # Lookahead penalty
        # lookahead_pen = self.lookahead_penalty(row, col, lookahead_steps)
        #
        # # Tổng heuristic
        return 0

    # Hành động thực hiện lên người chơi
    def move(self, state):
        x, y = state
        actions = []
        for dx, dy in DICHUYEN:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.num_rows and 0 <= ny < self.num_cols:
                if self.tt_bandau[nx, ny] != 1:
                    actions.append((nx, ny))
        return actions

    def BeliefSearch(self):
        self.reset_stats()
        start_time = time.time()
        goals_belief = set(self.goals)
        visited_list_beliefs = []

        list_curs_belief = [self.starts[:]]

        # Lưu cha để truy vết đường đi cho từng start
        cha_dicts = [{} for _ in range(self.starts_size)]


        visited_list_beliefs.append(self.starts[:])
        while list_curs_belief:
            curs_belief = list_curs_belief.pop()


            if any(not self.move(state) for state in curs_belief): # bỏ qua nếu một belief không đi được
                continue

            if all(state in goals_belief for state in curs_belief):
                for i, start in enumerate(self.starts):
                    goal = curs_belief[i]  # lấy trạng thái thứ i
                    if goal in cha_dicts[i]:
                        self.duong_di_belief[i] = self.tim_duongdi(start, goal, cha_dicts[i])
                    else:
                        self.duong_di_belief[i] = [start]
                self.Dodai_duongdi = [len(p) for p in self.duong_di_belief]
                self.execution_time = time.time() - start_time
                print("1\n")
                return self.list_tt_duyet_belief, self.duong_di_belief

            # tạo 4 tập belief mới rỗng
            new_beliefs = [[] for _ in range(4)]
            check = True
            for i, state in enumerate(curs_belief):
                self.list_tt_duyet_belief[i].append(state)
                self.So_tt_daduyet[i] += 1

                if state in goals_belief:# Nếu đã đạt goal --> giữ nguyên
                    for nb in new_beliefs:
                        nb.append(state)
                    continue

                # Sinh tập trạng thái con
                states_con = self.move(state)
                if not states_con:# Nếu ko có con --> break
                    check = False
                    self.visited_belief[i].add(state)
                    break

                # Lọc 2 trạng thái con tốt nhất
                states_con_sorted = sorted(states_con, key=self.heuristic)
                best_four = [s for s in states_con_sorted]
                while len(best_four) < 4 and len(best_four) >=1:
                    best_four.append(best_four[0])

                if not best_four:  # không có trạng thái con nào
                    check = False
                    break

                self.So_tt_dasinh[i] += len(best_four)
                for next_state in best_four:
                    cha_dicts[i][next_state] = state
                    self.visited_belief[i].add(state)

                # Gán trạng thái con vào 4 belief mới
                for j in range(4):
                    new_beliefs[j].append(best_four[j])

            # Ra ngoài vòng lặp kiểm tra 4 belief này
            if check:
                i=0
                for nb in new_beliefs:
                    # Kiểm tra xem belief này đã xuất hiện chưa
                    if nb not in visited_list_beliefs:
                        list_curs_belief.append(nb)
                        visited_list_beliefs.append(nb)
                        i+=1
                        if i ==1: break
                    print(nb,"\n")

        # nếu hết vòng mà vẫn chưa return
        self.execution_time = time.time() - start_time
        return self.list_tt_duyet_belief, []


class MapModel:
    def __init__(self):
        # 0 là ô trống, 1 là chướng ngại vật
        self.collision_matrix = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 3],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


# === Tạo bản đồ và đối tượng tìm kiếm ===
map_model = MapModel()

# Tập trạng thái khởi đầu (agent có thể ở 2 vị trí khác nhau ban đầu)
starts = [(1, 1), (1, 3)]

# Tập goal (2 vị trí đích khác nhau)
# Tập goal: tất cả các ô trống từ hàng 15 trở đi
goals = [(19,28),(19,27)]
belief = CES_BeliefSearch(map_model, starts, goals)
list_duyet, duong_di = belief.BeliefSearch()

print("Các trạng thái đã duyệt:")
print(list_duyet)
print("Đường đi đến đích:")
print(duong_di)
print("Thống kê:")
print(belief.thong_so())