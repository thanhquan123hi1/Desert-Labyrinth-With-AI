import numpy as np
from pympler import asizeof
import time

#Maze matrix
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

DICHUYEN = [(0,1),(1,0),(0,-1),(-1,0)]

class AndOrSearch:
    def __init__(self, ma_tran=None):
        if ma_tran is None:
            ma_tran = matrix
        self.tt_bandau = np.array(ma_tran)
        self.num_rows, self.num_cols = self.tt_bandau.shape

        #lưu thứ tự các trạng thái đã duyệt
        self.list_tt_duyet = []
        #lưu đường đi
        self.duong_di = []

        #Các thông số để so sánh
        self.So_tt_daduyet = 0  #số trạng thái đã duyệt
        self.So_tt_dasinh = 0  #số trạng thái đã sinh/được xem xét
        self.Kichthuoc_bonho = 0  #Số tt ở thời điểm stack max
        self.Kichthuoc_bonho_MB = 0.0  #kích thước bộ nhớ max
        self.Dodai_duongdi = 0  #chiều dài đường đi
        self.execution_time = 0  #thời gian thực thi

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

    #4. hành đọng thực hiện lên người chơi(chỉ có 1 là di chuyển)
    def hanhdongs(self, state):
        x, y = state
        actions = []
        for dx, dy in DICHUYEN:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.num_rows and 0 <= ny < self.num_cols:
                if self.tt_bandau[nx, ny] != 1:
                    actions.append((nx, ny))
        return actions

    #5. Duyệt qua node or --> sinh ra các TH có thể đi
    def or_search(self, state, path, cha):
        self.list_tt_duyet.append(state)
        self.So_tt_daduyet += 1

        if self.la_tt_goal(*state):
            return [state]

        if state in path:
            return None  #fail nếu tt đã tồn tại trên path

        for next_state in self.hanhdongs(state):
            self.So_tt_dasinh += 1
            #gọi node and vs từng tt cso thể
            subplan = self.and_search([next_state], path + [state], cha)
            if subplan is not None:  #nếu subplan thành công
                cha[next_state] = state
                return [state] + subplan  #trả về kế hoachwj

        return None  #fail nếu không có tt nào thành công

    #6. Duyệt qua node And ---> sinh ra tất cả các TH có thể xảy ra nếu như thực hiện bước đó
    def and_search(self, states, path, cha):
        #And node: tất cả tt phải thành công
        plans = []
        for s in states:
            self.list_tt_duyet.append(s)
            self.So_tt_daduyet += 1

            subplan = self.or_search(s, path, cha)
            if subplan is None:  #fail nếu 1 state trong And node fail
                return None
            plans.extend(subplan)

        return plans

    #7. chạy thuật toán
    def chay_thuattoan(self):
        start_time = time.time()
        start = self.tim_vitri(2)[0]
        cha = {}
        plan = self.or_search(start, [], cha)
        if plan:
            self.duong_di = plan
            self.Dodai_duongdi = len(plan)
        self.execution_time = time.time() - start_time
        return self.list_tt_duyet, self.duong_di

#-------- MAIN TEST --------
print("\n", "AndOrSearch".center(60, "-"))
mb = AndOrSearch()
a, b = mb.chay_thuattoan()
a = [(int(r), int(c)) for r,c in a]
b = [(int(r), int(c)) for r,c in b]
print("Trạng thái đã duyệt qua: ", a)
print("Đường đi: ", b)
print("Thông số:", mb.thong_so())
# Thông số: {
# 'So tt da duyet': 129,
# 'So tt da sinh': 64,
# 'Kich thuoc bo nho (tt)': 129,
# 'Kich thuoc bo nho (MB)': 0.008636,
# 'Do dai duong di': 51,
# 'Execution time (s)': 0.001772
# }