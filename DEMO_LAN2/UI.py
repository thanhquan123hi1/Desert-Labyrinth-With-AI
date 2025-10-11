import tkinter as tk
import numpy as np
from UninformedSearch import UninformedSearch
# --- MapModel ---
class MapModel:
    def __init__(self):
        self.collision_matrix = np.array([
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
])
        self.num_rows, self.num_cols = self.collision_matrix.shape

# --- Maze UI ---
class MazeUI:
    def __init__(self, master, map_model, start = (1,1), enemy = (18,28),
                 goals = [(19,29),(18,29),(17,28),(17,27)] , items=[(5,2),(5,4),(10,10)], traps=[(3,4),(7,7),(15,15)], health=3):
        self.master = master
        self.map_model = map_model
        self.player_pos = start
        self.enemy_pos = enemy
        self.goals = goals if goals else []
        self.items = items if items else []
        self.traps = traps if traps else []
        self.collected_items = set()
        self.health = health

        self.cell_size = 20  # giảm kích thước cho ma trận lớn
        self.canvas = tk.Canvas(master,
                                width=self.map_model.num_cols*self.cell_size,
                                height=self.map_model.num_rows*self.cell_size)
        self.canvas.pack()
        self.draw_map()

    def draw_map(self):
        self.canvas.delete("all")
        for i in range(self.map_model.num_rows):
            for j in range(self.map_model.num_cols):
                x0,y0 = j*self.cell_size, i*self.cell_size
                x1,y1 = x0+self.cell_size, y0+self.cell_size
                val = self.map_model.collision_matrix[i,j]
                if val==1:
                    color = "black"
                elif val==2:
                    color = "blue"  # start
                elif val==3:
                    color = "green"  # goal
                else:
                    color = "white"
                self.canvas.create_rectangle(x0,y0,x1,y1,fill=color)

        for tx,ty in self.traps:
            self.canvas.create_rectangle(ty*self.cell_size, tx*self.cell_size,
                                         (ty+1)*self.cell_size, (tx+1)*self.cell_size, fill="orange")
        for ix,iy in self.items:
            if (ix,iy) not in self.collected_items:
                self.canvas.create_rectangle(iy*self.cell_size, ix*self.cell_size,
                                             (iy+1)*self.cell_size, (ix+1)*self.cell_size, fill="yellow")

        # Enemy
        ex,ey = self.enemy_pos
        self.canvas.create_oval(ey*self.cell_size, ex*self.cell_size,
                                (ey+1)*self.cell_size, (ex+1)*self.cell_size, fill="red")
        # Player
        px,py = self.player_pos
        self.canvas.create_oval(py*self.cell_size, px*self.cell_size,
                                (py+1)*self.cell_size, (px+1)*self.cell_size, fill="blue")

    def update_positions(self, player_pos, enemy_pos):
        self.player_pos = player_pos
        self.enemy_pos = enemy_pos

        # Trap check
        if player_pos in self.traps:
            self.health -=1
            print(f"Player gặp Trap tại {player_pos}, máu còn {self.health}")

        # Item check
        if player_pos in self.items and player_pos not in self.collected_items:
            self.collected_items.add(player_pos)
            print(f"Player thu thập Item tại {player_pos}")

        # Goal check
        if player_pos in self.goals or self.map_model.collision_matrix[player_pos]==3:
            print(f"Player đạt Goal tại {player_pos}")

        # Enemy check
        if player_pos == enemy_pos:
            print(f"GAME OVER! Player gặp Enemy tại {player_pos}")
        self.draw_map()

"""Test cho UI"""
#
# # --- Demo ---
# root = tk.Tk()
# root.title("Maze Game Demo")
#
# map_model = MapModel()
#
# # Start, enemy và goal lấy từ ma trận
# start = (1,1)
# enemy = (18,28)
#
# ui = MazeUI(root, map_model)
#
# # Demo path ngắn (phải tự tạo theo ma trận mới)
# # --- Tạo path_player dài 100 bước ---
# path_player = []
# pos = start
# # Ví dụ path zig-zag nhỏ, tránh tường
# directions = [(0,1),(1,0),(0,1),(1,0),(0,1),(1,0),(0,1),(1,0)]
# for i in range(100):
#     dx,dy = directions[i % len(directions)]
#     new_pos = (pos[0]+dx, pos[1]+dy)
#     # kiểm tra không ra ngoài hoặc chạm tường
#     if 0 <= new_pos[0] < map_model.num_rows and 0 <= new_pos[1] < map_model.num_cols:
#         if map_model.collision_matrix[new_pos] != 1:
#             pos = new_pos
#     path_player.append(pos)
#
# # --- Tạo path_enemy dài 100 bước ---
# path_enemy = []
# pos = enemy
# directions = [(0,-1),(-1,0),(0,-1),(-1,0),(0,-1),(-1,0)]
# for i in range(100):
#     dx,dy = directions[i % len(directions)]
#     new_pos = (pos[0]+dx, pos[1]+dy)
#     if 0 <= new_pos[0] < map_model.num_rows and 0 <= new_pos[1] < map_model.num_cols:
#         if map_model.collision_matrix[new_pos] != 1:
#             pos = new_pos
#     path_enemy.append(pos)
#
# for i in range(len(path_player)):
#     def step(i=i):
#         if i<len(path_enemy):
#             enemy_pos = path_enemy[i]
#         else:
#             enemy_pos = enemy
#         player_pos = path_player[i]
#         ui.update_positions(player_pos, enemy_pos)
#     root.after(200*i, step)
#
# root.mainloop()
"""Test cho BFS"""
# def test_bfs_with_ui():
#     root = tk.Tk()
#     root.title("Maze BFS Test")
#
#     map_model = MapModel()
#
#     # Khởi tạo UI
#     ui = MazeUI(root, map_model,
#                 start=(1,1),
#                 enemy=(18,28),
#                 goals=[(1, 27), (19, 28), (19, 1)],
#                 items=[(5, 2), (5, 4), (11, 10)],
#                 traps=[(3,4),(7,7),(15,15)],
#                 health=3)
#
#     # Khởi tạo BFS search
#     search = UninformedSearch(
#         map_model,
#         start=(1,1),
#         enemy_start=(18,28),
#         goals = [(1, 27), (19, 28), (19, 1)],
#         items = [(5, 2), (5, 4), (11, 10)],
#         traps=[(3,4),(7,7),(15,15)],
#         max_health=3
#     )
#
#     # Chạy BFS
#     player_path, enemy_path = search.search_multiple_goals()
#
#     # Hàm chạy từng bước lên UI
#     def step(i=0):
#         if i < len(player_path):
#             ui.update_positions(player_path[i], enemy_path[i])
#             root.after(200, lambda: step(i+1))
#
#     step()  # bắt đầu chạy
#     root.mainloop()
# test_bfs_with_ui()
"""Test cho DFS"""
# def test_dfs_with_ui():
#     import tkinter as tk
#     from UninformedSearch import MapModel, UninformedSearch
#     import time
#
#     root = tk.Tk()
#     root.title("Maze DFS Test")
#
#     map_model = MapModel()
#
#     # Khởi tạo UI
#     ui = MazeUI(root, map_model,
#                 start=(1,1),
#                 enemy=(18,28),
#                 goals=[(1, 27), (19, 28), (19, 1)],
#                 items = [(5, 2), (5, 4), (11, 10)],
#                 traps=[(3,4),(7,7),(15,15)],
#                 health=3)
#
#     # Khởi tạo DFS search
#     search = UninformedSearch(
#         map_model,
#         start=(1,1),
#         enemy_start=(18,28),
#         goals=[(1, 27), (19, 28), (19, 1)],
#         items=[(5, 2), (5, 4), (11, 10)],
#         traps=[(3,4),(7,7),(15,15)],
#         max_health=3
#     )
#
#     # Chạy DFS
#     player_path, enemy_path = search.search_multiple_goals(method="DFS")
#
#     # Hàm chạy từng bước lên UI
#     def step(i=0):
#         if i < len(player_path):
#             ui.update_positions(player_path[i], enemy_path[i])
#             root.after(200, lambda: step(i+1))
#
#     step()  # bắt đầu chạy
#     root.mainloop()
# test_dfs_with_ui()
"""Test cho A* (Informed Search)"""
# def test_astar_with_ui():
#     from InformedSearch import InformedSearch  # dùng nhóm Informed
#
#     root = tk.Tk()
#     root.title("Maze A* Test")
#
#     # --- Khởi tạo bản đồ ---
#     map_model = MapModel()
#
#     # --- Cấu hình trò chơi ---
#     start = (1, 1)
#     enemy_start = (18, 28)
#     goals = [(1, 27), (19, 28), (19, 1)]
#     items = [(5, 2), (5, 4), (11, 10)]
#     traps = [(3, 4), (7, 7), (15, 15)]
#     max_health = 3
#
#     # --- Khởi tạo UI ---
#     ui = MazeUI(
#         root,
#         map_model,
#         start=start,
#         enemy=enemy_start,
#         goals=goals,
#         items=items,
#         traps=traps,
#         health=max_health
#     )
#
#     # --- Khởi tạo thuật toán A* ---
#     search = InformedSearch(
#         map_model,
#         start=start,
#         enemy_start=enemy_start,
#         goals=goals,
#         items=items,
#         traps=traps,
#         max_health=max_health
#     )
#
#     # --- Chạy tìm đường bằng A* ---
#     player_path, enemy_path = search.search_multiple_goals(method="Astar")
#
#     # --- In thông số ---
#     print("=== THÔNG SỐ THUẬT TOÁN A* ===")
#     for key, value in search.thong_so().items():
#         print(f"{key}: {value}")
#
#     # --- Hàm di chuyển từng bước trên UI ---
#     def step(i=0):
#         if i < len(player_path):
#             ui.update_positions(player_path[i], enemy_path[i])
#             root.after(200, lambda: step(i + 1))
#         else:
#             print("Hoàn thành đường đi.")
#
#     # --- Bắt đầu mô phỏng ---
#     step()
#     root.mainloop()
# test_astar_with_ui()
#
