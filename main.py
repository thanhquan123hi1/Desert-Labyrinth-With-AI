import pygame, sys

from Astar import AStar
from BFS import BFS
from BeamSearch import BeamSearch
from Button import Button
from DFS import DFS
from Dropdown import Dropdown
from Greedy import Greedy
from SimulatedAnnealing import SimulatedAnnealing
from settings import RES, X_START, Y_START, X_GOAL, Y_GOAL #import kích thước của màn hình  ******************
from map_model import MapModel #import các class MapModel và Player
from player import Player

# 2: vị trí nhân vật
# 3: vị trí goal

class App:   #Để chạy chương trình chính(xử lý sự kiện)
    def __init__(self):
        #Các khởi tạo màn hình pygame đơn giản
        pygame.init()
        self.surface = pygame.display.set_mode(RES)
        pygame.display.set_caption("MAZE")
        self.clock = pygame.time.Clock()

        #Tạo đối tượng MapModel và Player
        self.map_model = MapModel("Resources/Maps/Map1.tmx")
        self.player_group = pygame.sprite.Group()  #Tạo ra một đối tượng nhóm để quản lí tất cả các sprite(tile)

        self.player = Player((X_START*32, Y_START*32) , self.player_group) #đưa vào nhóm ******************

        self.start_matrix = self.map_model.collision_matrix
        self.start_matrix[X_START][Y_START] = 2
        self.start_matrix[X_GOAL][Y_GOAL] = 3

        self.list_tt, self.duong_di = [], []
        self.step_index = 0
        self.path_index = 0
        self.option_algs = ["BFS", "DFS", "Greedy", "AStar", "BeamSearch", "SimulatedAnnealing"]
        # Dropdown chọn thuật toán
        font = pygame.font.SysFont(None, 24)
        self.dropdown = Dropdown(31*32, 1*32, 150, 30, font, (50, 50, 50), (100, 100, 100), self.option_algs)

        self.reset_button = Button(36*32, 1*32, 80, 30, "Reset", font, (70, 70, 70), (120, 120, 120))

        self.reset()

    def reset(self):
        # Reset player về vị trí start
        self.player_group.empty()
        self.player = Player((X_START * 32, Y_START * 32), self.player_group)

        # Reset map: làm lại collision_matrix
        self.start_matrix = self.map_model.collision_matrix
        self.start_matrix[X_START][Y_START] = 2
        self.start_matrix[X_GOAL][Y_GOAL] = 3

        # Reset dữ liệu thuật toán
        self.list_tt, self.duong_di = [], []
        self.step_index = 0
        self.path_index = 0

        # Reset dropdown về mặc định
        self.dropdown.active_option = "Algorithms"

    def run_algorithm(self, algo_name):
        if algo_name == "BFS":
            algo = BFS(self.start_matrix)
        elif algo_name == "DFS":
            algo = DFS(self.start_matrix)
        elif algo_name == "Greedy":
            algo = Greedy(self.start_matrix)
        elif algo_name == "AStar":
            algo = AStar(self.start_matrix)
        elif algo_name == "BeamSearch":
            algo = BeamSearch(self.start_matrix)
        elif algo_name == "SimulatedAnnealing":
            algo = SimulatedAnnealing(self.start_matrix)
        elif algo_name == "DFS":
            algo = DFS(self.start_matrix)
        else:
            return
        self.list_tt, self.duong_di = algo.chay_thuattoan()

    def draw(self):
        self.surface.fill("black") #Vẽ nền
        self.map_model.draw(self.surface) #Vẽ Map
        self.player_group.draw(self.surface) #Vẽ nhóm sprite
        self.dropdown.draw(self.surface) #Vẽ combobox
        self.reset_button.draw(self.surface) #Nút reset

    # Hàm xử lí xự kiện
    def run(self):
        while True:
            dt = self.clock.tick(20) / 1000 #tối đa 10 khung hình 1s
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                selected = self.dropdown.handle_event(e)
                if selected:
                    self.run_algorithm(selected)

                if self.reset_button.handle_event(e):
                    self.reset()

            self.player_group.update(dt, self.map_model.collision_matrix) #update các lại vị trí theo sự di chuyển
            self.map_model.update(dt) #update lại map (nếu như là map động)

            self.draw() #Sau khi cập nhật xong các giá trị tọa độ hay là các sprite động
            self.draw_steps()
            self.draw_paths()
            pygame.display.set_caption("Map: " + str(round(self.clock.get_fps())))

            # Tăng chỉ số bước mỗi khung hình
            if self.step_index < len(self.list_tt):
                self.step_index += 1

            if self.step_index >= len(self.list_tt) and self.path_index < len(self.duong_di):
                self.path_index += 1

            pygame.display.flip()  #hiển thị hết lên màn hình

    def draw_steps(self):
        tile_w, tile_h = self.map_model.map_data.tilewidth, self.map_model.map_data.tileheight

        # Vẽ các ô đã duyệt đến step_index
        for i in range(self.step_index):
            row, col = self.list_tt[i]
            rect = pygame.Rect(col * tile_w, row * tile_h, tile_w, tile_h)
            pygame.draw.rect(self.surface, (0, 0, 255), rect)  # xanh dương: ô đã duyệt

    def draw_paths(self):
        tile_w, tile_h = self.map_model.map_data.tilewidth, self.map_model.map_data.tileheight
        # Nếu BFS tìm được đường đi, vẽ đường đi màu vàng
        for i in range(self.path_index):
            row, col = self.duong_di[i]
            rect = pygame.Rect(col * tile_w, row * tile_h, tile_w, tile_h)
            pygame.draw.rect(self.surface, (255, 255, 0), rect)

if __name__ == "__main__":
    app = App()
    app.run()
