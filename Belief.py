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

#Các hướng di chuyển:
DICHUYEN = [(-1, 0), (0, -1), (0, 1), (1, 0)]


class Belief:
    def __init__(self, ma_tran=None, belief_size=2):
        self.tt_bandau = np.array(ma_tran if ma_tran is not None else matrix)
        self.tt_bandau[1, 3] = 2
        self.tt_bandau[4, 4] = 2
        self.num_rows, self.num_cols = self.tt_bandau.shape

        #Thông số
        self.So_tt_daduyet = 0
        self.So_tt_dasinh = 0
        self.Kichthuoc_bonho = 0
        self.Kichthuoc_bonho_MB = 0.0
        self.Dodai_duongdi = 0
        self.execution_time = 0

        self.belief_size = belief_size  #số lượng trạng thái ban đầu
        self.belief = []  #tập trạng thái hiện tại

        #Lưu riêng list_tt_duyet và duong_di cho từng trạng thái
        self.list_tt_duyet_belief = [[] for _ in range(belief_size)]
        self.duong_di_belief = [[] for _ in range(belief_size)]

        self.visited_belief = [set() for _ in range(belief_size)]
        self.memo = {}  #lưu kết quả DFS của từng state

        self.trangthai_laplai = {}

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
        self.Kichthuoc_bonho = sum(len(lst) for lst in self.list_tt_duyet_belief)
        self.Kichthuoc_bonho_MB = asizeof.asizeof(self.list_tt_duyet_belief) / (1024 ** 2)
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

    #5. DFS trên một trạng thái, lưu list_tt_duyet và duong_di riêng, dùng memoization
    def dfs_state(self, state, idx):
        if state in self.memo:  #nếu đã DFS state này rồi
            return self.memo[state]

        self.list_tt_duyet_belief[idx].append(state)  #ghi lại trạng thái đã duyệt
        self.So_tt_daduyet += 1
        if self.la_tt_goal(*state):
            self.duong_di_belief[idx] = [state]
            self.memo[state] = [state]
            return [state]

        self.visited_belief[idx].add(state)
        for next_state in reversed(self.hanhdongs(state)):
            self.So_tt_dasinh += 1

            # Kiểm tra nếu next_state đã có trong visited của belief khác
            for j in range(self.belief_size):
                if j != idx and next_state in self.visited_belief[j]:
                    # Ghi lại trạng thái lặp lại và belief đã tạo ra nó
                    self.trangthai_laplai[idx] = (next_state, j)
                    # Ghi lại đường đi đến đó
                    self.duong_di_belief[idx] = self.duong_di_belief[idx] + [next_state]
                    # Ngưng belief này
                    return self.duong_di_belief[idx]

            # Nếu next_state chưa duyệt trong belief hiện tại
            if next_state not in self.visited_belief[idx]:
                subplan = self.dfs_state(next_state, idx)
                if subplan is not None:
                    duongdi = [state] + subplan
                    self.duong_di_belief[idx] = duongdi
                    self.memo[state] = duongdi
                    return duongdi

        self.memo[state] = None  #không tìm được đường đi
        return None  #fail nếu không còn hành động

    #6. Cập nhật belief bằng DFS
    def capnhat_belief(self):
        for i, state in enumerate(self.belief):
            if self.la_tt_goal(*state):  #Nếu trạng thái đã đạt goal thì giữ nguyên, không xét hành động nữa
                continue
            subplan = self.dfs_state(state, i)
            if subplan is None:  #Nếu DFS thất bại với state này --> fail
                return None
            self.belief[i] = subplan[-1]  #Lấy trạng thái cuối cùng DFS tìm được
        return self.belief

    #---------------Chạy  Belief --------------
    def chay_thuattoan(self):
        start_time = time.time()
        start_candidates = self.tim_vitri(2)[:self.belief_size]  #chọn n trạng thái ban đầu
        self.belief = start_candidates

        while True:
            if all(self.la_tt_goal(*s) for s in self.belief):  #Nếu tất cả trạng thái đã đạt goal
                self.Dodai_duongdi = sum(len(d) for d in self.duong_di_belief)
                self.execution_time = time.time() - start_time
                return self.list_tt_duyet_belief[0], self.duong_di_belief[0]  #sửa lại bỏ [0] nếu vào UI

            updated = self.capnhat_belief()
            if updated is None:  #Nếu một trạng thái không còn hành động khả thi --> fail
                self.execution_time = time.time() - start_time
                return self.list_tt_duyet_belief, None


#-------- MAIN TEST --------
print("\n", "Belief--DFS".center(60, "-"))
mb = Belief()
list_tt, list_duongdi = mb.chay_thuattoan()
print("Trạng thái đã duyệt qua từng belief: ", list_tt)
print("Đường đi từng belief: ", list_duongdi)
print("Thông số:", mb.thong_so())
# Thông số SimulatedAnnealing: {
# 'So tt da duyet': 46,
# 'So tt da sinh': 71,
# 'Kich thuoc bo nho (tt)': 3,
# 'Kich thuoc bo nho (MB)': 0.000443,
# 'Do dai duong di': 47,
# 'Execution time (s)': 0.017633
# }
