import numpy as np
from pympler import asizeof
import time

matrix = [
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
]

#Các hướng di chuyển: right, down, left, up
DICHUYEN = [(0, 1), (1, 0), (0, -1), (-1, 0)]

class BeliefGreedy:
    def __init__(self, ma_tran=None, belief_size=2):
        self.tt_bandau = np.array(ma_tran if ma_tran is not None else matrix)
        self.tt_bandau[1, 3] = 2
        self.tt_bandau[4, 4] = 2
        self.num_rows, self.num_cols = self.tt_bandau.shape
        self.list_tt_duyet = []
        self.duong_di = []

        #Thông số
        self.So_tt_daduyet = 0
        self.So_tt_dasinh = 0
        self.Kichthuoc_bonho = 0
        self.Kichthuoc_bonho_MB = 0.0
        self.Dodai_duongdi = 0
        self.execution_time = 0

        self.belief_size = belief_size  #số lượng trạng thái ban đầu
        self.belief = []  #tập trạng thái hiện tại

    #1. Tìm tập vị trí có giá trị trong ma trận bằng giá trị
    def tim_vitri(self, gia_tri):
        list_toado = np.argwhere(self.tt_bandau == gia_tri)
        return [tuple(p) for p in list_toado]

    #2. kiểm tra là goal
    def la_tt_goal(self, row, col):
        goal = self.tim_vitri(3)[0]
        return (row, col) == goal

    #3. Thông số
    def thong_so(self):
        self.Kichthuoc_bonho = len(self.list_tt_duyet)
        self.Kichthuoc_bonho_MB = asizeof.asizeof(self.list_tt_duyet) / (1024 ** 2)
        return {
            "So tt da duyet": self.So_tt_daduyet,
            "So tt da sinh": self.So_tt_dasinh,
            "Kich thuoc bo nho (tt)": self.Kichthuoc_bonho,
            "Kich thuoc bo nho (MB)": round(self.Kichthuoc_bonho_MB, 6),
            "Do dai duong di": self.Dodai_duongdi,
            "Execution time (s)": round(self.execution_time, 6)
        }

    #4. hành động thực hiện lên người chơi(chỉ có 1 là di chuyển)
    def hanhdongs(self, state):
        x, y = state
        actions = []
        for dx, dy in DICHUYEN:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.num_rows and 0 <= ny < self.num_cols:
                if self.tt_bandau[nx, ny] != 1:
                    actions.append((nx, ny))
        return actions

    #5. Hàm heuristic Greedy: chọn ô gần goal nhất
    def heuristic(self, state):
        goal = self.tim_vitri(3)[0]
        x, y = state
        gx, gy = goal
        return abs(gx - x) + abs(gy - y)  #Manhattan distance

    #6. Cập nhật belief từng bước theo Greedy
    def cap_nhat_belief(self):
        new_belief = []
        for state in self.belief:
            if self.la_tt_goal(*state): #Nếu trạng thái đã đạt goal thì giữ nguyên, không xét hành động nữa
                new_belief.append(state)
                continue

            actions = self.hanhdongs(state)
            self.So_tt_daduyet += 1
            if not actions:   #Nếu trạng thái này không có hành động nào khả thi ---> fail
                return None
            self.So_tt_dasinh += len(actions)

            best_action = min(actions, key=self.heuristic)  #Chọn hành động Greedy (gần goal nhất)
            new_belief.append(best_action)
        self.list_tt_duyet.extend(self.belief)
        self.belief = new_belief
        return self.belief

    #Chạy thuật toán Belief Greedy
    def chay_thuattoan(self):
        start_time = time.time()
        start_candidates = self.tim_vitri(2)[:self.belief_size]  #chọn n trạng thái ban đầu(tự chọn nếu random thì phải viết hàm để tránh random vào dead_end)
        self.belief = start_candidates
        goal_reached = [False] * len(self.belief)

        while True:
            if all(self.la_tt_goal(*s) for s in self.belief): #Nếu tất cả trạng thái đã đạt goal
                self.duong_di = self.belief
                self.Dodai_duongdi = len(self.belief)
                self.execution_time = time.time() - start_time
                return self.list_tt_duyet, self.duong_di

            updated = self.cap_nhat_belief()
            if updated is None: #Nếu một trạng thái không còn hành động khả thi --> fail
                self.execution_time = time.time() - start_time
                return self.list_tt_duyet, None


#-------- MAIN TEST --------
print("\n", "Belief--Greedy".center(60, "-"))
mb = BeliefGreedy()
a, b = mb.chay_thuattoan()
a = [(int(r), int(c)) for r, c in a]
b = [(int(r), int(c)) for r, c in b]
print("Trạng thái đã duyệt qua: ", a)
print("Đường đi: ", b)
print("Thông số:", mb.thong_so())
