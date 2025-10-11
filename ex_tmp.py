import tkinter as tk
import numpy as np

# --- MapModel ---
class MapModel:
    def __init__(self):
        self.collision_matrix = np.array([
            [1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,1,0,0,0,0,1],
            [1,0,1,0,1,0,1,1,0,1],
            [1,0,1,0,0,0,0,1,0,1],
            [1,0,1,1,1,1,0,1,0,1],
            [1,0,0,0,0,1,0,0,0,1],
            [1,1,1,0,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,1,0,1],
            [1,0,1,1,1,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1],
        ])
        self.num_rows, self.num_cols = self.collision_matrix.shape

# --- Maze UI ---
class MazeUI:
    def __init__(self, master, map_model, start, enemy, goals=None, items=None, traps=None, health=3):
        self.master = master
        self.map_model = map_model
        self.player_pos = start
        self.enemy_pos = enemy
        self.goals = goals if goals else []
        self.items = items if items else []
        self.traps = traps if traps else []
        self.collected_items = set()
        self.health = health

        self.cell_size = 50
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
                color = "black" if self.map_model.collision_matrix[i,j]==1 else "white"
                self.canvas.create_rectangle(x0,y0,x1,y1,fill=color)

        for tx,ty in self.traps:
            self.canvas.create_rectangle(ty*self.cell_size, tx*self.cell_size,
                                         (ty+1)*self.cell_size, (tx+1)*self.cell_size, fill="orange")
        for ix,iy in self.items:
            if (ix,iy) not in self.collected_items:
                self.canvas.create_rectangle(iy*self.cell_size, ix*self.cell_size,
                                             (iy+1)*self.cell_size, (ix+1)*self.cell_size, fill="yellow")
        for gx,gy in self.goals:
            self.canvas.create_rectangle(gy*self.cell_size, gx*self.cell_size,
                                         (gy+1)*self.cell_size, (gx+1)*self.cell_size, fill="green")
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
        if player_pos in self.goals:
            print(f"Player đạt Goal tại {player_pos}")

        # Enemy check
        if player_pos == enemy_pos:
            print(f"GAME OVER! Player gặp Enemy tại {player_pos}")

        self.draw_map()


# --- Demo ---
root = tk.Tk()
root.title("Maze Game Demo")

map_model = MapModel()
ui = MazeUI(root, map_model,
            start=(1,1),
            enemy=(7,7),
            goals=[(7,8)],
            items=[(1,2),(5,2)],
            traps=[(2,3),(5,4)],
            health=3)

# Sample paths
path_player = [(1,1),(1,2),(2,2),(2,3),(3,3),(4,3),(5,3),(5,4),(6,4),(7,4),(7,5),(7,6),(7,7),(7,8)]
path_enemy  = [(7,7),(6,7),(5,7),(4,7),(3,7),(2,7),(1,7),(1,6),(1,5),(1,4),(2,4),(3,4),(4,4),(5,4)]

for i in range(len(path_player)):
    def step(i=i):
        player_pos = path_player[i]
        enemy_pos = path_enemy[i]
        ui.update_positions(player_pos, enemy_pos)
    root.after(500*i, step)

root.mainloop()
