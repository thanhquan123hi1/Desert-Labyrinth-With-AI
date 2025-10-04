import numpy as np
import time
from pympler import asizeof
from collections import deque

# tt: trạng thái
# 2: vị trí nhân vật (start)
# 3: vị trí goal

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

class BacktrackingForwardChecking:
    def __init__(self, ma_tran=None):
        if ma_tran is None:
            ma_tran = matrix
        self.tt_bandau = np.array(ma_tran)
        self.num_rows, self.num_cols = self.tt_bandau.shape

        # lưu thứ tự các trạng thái đã duyệt (theo thứ tự 'visit')
        self.list_tt_duyet = []
        # lưu đường đi (nếu tìm được)
        self.duong_di = []

        # Các thông số để so sánh
        self.So_tt_daduyet = 0  # số trạng thái đã duyệt
        self.So_tt_dasinh = 0   # số trạng thái đã sinh/được xem xét
        self.Kichthuoc_bonho = 0  # Số tt ở thời điểm stack/stack-like max (độ sâu tối đa)
        self.Kichthuoc_bonho_MB = 0.0 # kích thước bộ nhớ max (MB)
        self.Dodai_duongdi = 0  # chiều dài đường đi
        self.execution_time = 0  # thời gian thực thi

    # 1. Tìm tập vị trí có giá trị trong ma trận bằng giá trị(cần xét)
    def tim_vitri(self, gia_tri):
        list_toado = np.argwhere(self.tt_bandau == gia_tri)
        return [tuple(p) for p in list_toado]

    # 2. Sinh các trạng thái con hợp lệ (bỏ qua walls và visited)
    def sinh_tt_con(self, x, y, visited):
        list_tt_con = []
        for i,j in DICHUYEN:
            x1, y1 = x + i, y + j
            if 0 <= x1 < self.num_rows and 0 <= y1 < self.num_cols:
                if self.tt_bandau[x1, y1] != 1 and (x1, y1) not in visited:
                    list_tt_con.append((x1, y1))
        return list_tt_con

    # 3. Forward checking: kiểm tra xem từ vị trí (x,y) có tồn tại đường tới goal
    #    khi không được đi vào các ô trong 'visited' (những ô đã dùng trên đường hiện tại)
    def reachable_to_goal(self, start, goal, visited):
        # BFS nhanh chỉ trên ô chưa visited và không phải wall
        q = deque([start])
        seen = {start}
        while q:
            cur = q.popleft()
            if cur == goal:
                return True
            for nx, ny in self.sinh_tt_con(cur[0], cur[1], seen.union(visited)):
                if (nx, ny) not in seen:
                    seen.add((nx, ny))
                    q.append((nx, ny))
        return False

    # 4. Hàm đệ quy backtracking với forward checking
    def backtrack(self, cur, goal, visited, path):
        # cập nhật bộ nhớ max (dựa trên độ sâu / kích thước path)
        self.Kichthuoc_bonho = max(self.Kichthuoc_bonho, len(path))
        # tính kích thước bộ nhớ hiện tại của cấu trúc path để cập nhật MB
        try:
            size_MB = asizeof.asizeof(path) / (1024 * 1024)
            self.Kichthuoc_bonho_MB = max(self.Kichthuoc_bonho_MB, size_MB)
        except Exception:
            pass

        # đánh dấu đã duyệt (visit) hiện tại (lưu thứ tự duyệt)
        self.list_tt_duyet.append(cur)
        self.So_tt_daduyet += 1

        if cur == goal:
            # tìm được goal
            self.duong_di = path.copy()
            self.Dodai_duongdi = len(self.duong_di)
            return True

        # Sinh các trạng thái con
        children = self.sinh_tt_con(cur[0], cur[1], visited)
        # tăng số trạng thái đã sinh (đếm các con được tạo)
        self.So_tt_dasinh += len(children)

        # (không random để đảm bảo deterministic; nếu muốn random thì shuffle(children))
        for child in children:
            # forward checking: từ child có thể tới goal không nếu đánh dấu visited hiện tại + child?
            visited.add(child)
            can_reach = self.reachable_to_goal(child, goal, visited)
            if can_reach:
                path.append(child)
                found = self.backtrack(child, goal, visited, path)
                if found:
                    return True
                path.pop()
            # nếu không reach hoặc không tìm được ở nhánh này thì backtrack
            visited.remove(child)

        # khi rời node này (không tìm thấy) không xoá lịch sử liệt kê đã duyệt
        # (để giữ list_tt_duyet giống BFS là lịch sử duyệt), nhưng nếu bạn muốn
        # loại trạng thái khi backtrack thì có thể pop() ở đây.
        return False

    # --------- Chạy thuật toán (giao diện giống BFS) ----------
    def chay_thuattoan(self):
        start_time = time.time()

        starts = self.tim_vitri(2)
        goals = self.tim_vitri(3)
        if not starts or not goals:
            return None
        start = starts[0]
        goal = goals[0]

        # khởi tạo
        visited = {start}
        path = [start]

        # gọi backtracking + forward checking
        found = self.backtrack(start, goal, visited, path)

        self.execution_time = time.time() - start_time

        # nếu tìm được, self.duong_di đã được gán
        if found:
            # giống BFS gốc của bạn: loại bỏ start đầu tiên khỏi list_tt_duyet và duong_di khi in ra
            return self.list_tt_duyet, self.duong_di
        else:
            return self.list_tt_duyet, []

    # 6. Thông số
    def thong_so(self):
        return {
            "So tt da duyet": self.So_tt_daduyet,
            "So tt da sinh": self.So_tt_dasinh,
            "Kich thuoc bo nho (tt)": self.Kichthuoc_bonho,
            "Kich thuoc bo nho (MB)": round(self.Kichthuoc_bonho_MB, 6),
            "Do dai duong di": self.Dodai_duongdi,
            "Execution time (s)": round(self.execution_time, 6)
        }

if __name__ == "__main__":
    print("\n","Backtracking + Forward Checking (Maze)".center(60, "-"))
    solver = BacktrackingForwardChecking()
    a, b = solver.chay_thuattoan()

    # ép kiểu tất cả tuple (row, col) trong a và b thành int (giống BFS)
    a = [(int(row), int(col)) for row, col in a]
    b = [(int(row), int(col)) for row, col in b]

    print("Trạng thái đã duyệt qua:   ", a)
    print("Đường đi:   ", b)
    print("Thông số:", solver.thong_so())
