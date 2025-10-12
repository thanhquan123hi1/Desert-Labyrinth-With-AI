import pygame, sys
import numpy as np
from settings import RES, TILE_SIZE
from map_model import MapModel
from player import Player
from ui import UIManager
from Package_Menu import Menu, Options
from Package_Algorithm import UninformedSearch, InformedSearch, LocalSearch, AlgorithmPanel
from Package_Algorithm import NOOBS, find_start_beliefs, find_goal_beliefs
from Package_Animation import Particles
from Package_Panel import SolveHistoryPanel, PathViewPanel, ChartPanel


class App:
    def __init__(self, config):
        pygame.init()
        self.surface = pygame.display.set_mode(RES)
        pygame.display.set_caption("MAZE")
        self.clock = pygame.time.Clock()

        # --- Background ---
        self.bg = pygame.image.load(config["background"]).convert()
        self.bg = pygame.transform.scale(self.bg, RES)

        # --- Map ---
        self.map_offset = (32, 32)
        self.map_model = MapModel(config["map"], offset=self.map_offset)

        # --- UI ---
        self.ui = UIManager()

        # --- Hiệu ứng môi trường ---
        self.particles = Particles()
        self.effect = config.get("effect", "baocat")

        # --- Player ---
        self.player_group = pygame.sprite.Group()
        self.player = Player(
            (self.map_offset[0] + 32, self.map_offset[1] + 32),
            self.player_group,
            sprite_idle=config["player"]["idle"],
            sprite_run=config["player"]["run"],
            offset=self.map_offset
        )

        # --- Buttons ---
        self.imgNormal = pygame.image.load("Resources/Menu/buttons/btn_bhover.png").convert_alpha()
        self.imgHover = pygame.image.load("Resources/Menu/buttons/btn_yhover.png").convert_alpha()
        self.imgPressed = pygame.image.load("Resources/Menu/buttons/btn_bpressed.png").convert_alpha()

        self.imgNormal_back = pygame.image.load("Resources/Maps/buttons/back_normal.png").convert_alpha()
        self.imgHover_back = pygame.image.load("Resources/Maps/buttons/back_hover.png").convert_alpha()
        self.imgPressed_back = pygame.image.load("Resources/Maps/buttons/back_pressed.png").convert_alpha()

        # --- Panel thuật toán ---
        self.alg_panel = AlgorithmPanel()

        # --- Bộ nhớ kết quả & các panel overlay ---
        self.solve_history = []
        self.history_panel = SolveHistoryPanel()
        self.path_panel = PathViewPanel()
        self.chart_panel = ChartPanel()

    # ----------------------------------------------------------
    def draw_cells(self, cells, color_rgba):
        """Hàm này hỗ trợ cả list[(r,c)] và list[frozenset((r,c))]"""
        for item in cells:
            # Nếu phần tử là 1 belief (set hoặc frozenset)
            if isinstance(item, (set, frozenset, list)):
                for (r, c) in item:
                    rect = pygame.Rect(c * TILE_SIZE + self.map_offset[0],
                                       r * TILE_SIZE + self.map_offset[1],
                                       TILE_SIZE, TILE_SIZE)
                    s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                    s.fill(color_rgba)
                    self.surface.blit(s, rect.topleft)
            else:
                # Trường hợp thông thường
                (r, c) = item
                rect = pygame.Rect(c * TILE_SIZE + self.map_offset[0],
                                   r * TILE_SIZE + self.map_offset[1],
                                   TILE_SIZE, TILE_SIZE)
                s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                s.fill(color_rgba)
                self.surface.blit(s, rect.topleft)


    # ----------------------------------------------------------
    def run(self):
        start = (int((self.player.rect.centery - self.map_offset[1]) // TILE_SIZE),
                 int((self.player.rect.centerx - self.map_offset[0]) // TILE_SIZE))
        goal = (19, 28)
        print(f"Start: {start}, Goal: {goal}")

        search = None
        visited_states, path = [], []
        visible_visited, visible_path = [], []
        phase = "idle"

        v_ptr = p_ptr = move_idx = 0
        visited_timer = path_timer = move_timer = 0.0
        VISITED_INTERVAL, PATH_INTERVAL, MOVE_INTERVAL = 0.02, 0.05, 0.05

        def snap_to_start():
            sr, sc = start
            self.player.rect.center = (sc * TILE_SIZE + self.map_offset[0] + TILE_SIZE // 2,
                                       sr * TILE_SIZE + self.map_offset[1] + TILE_SIZE // 2)

        # =====================================================
        while True:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    mouse_click = True
                self.history_panel.handle_event(e)
                self.path_panel.handle_event(e)

            dt = self.clock.tick(60) / 1000.0

            # --- Update Animation ---
            if phase == "show_visited":
                visited_timer += dt
                while visited_timer >= VISITED_INTERVAL and v_ptr < len(visited_states):
                    visible_visited.append(visited_states[v_ptr])
                    v_ptr += 1
                    visited_timer -= VISITED_INTERVAL
                if v_ptr >= len(visited_states):
                    phase = "show_path"
                    p_ptr = 0
                    visible_path.clear()

            elif phase == "show_path":
                path_timer += dt
                while path_timer >= PATH_INTERVAL and p_ptr < len(path):
                    visible_path.append(path[p_ptr])
                    p_ptr += 1
                    path_timer -= PATH_INTERVAL
                if p_ptr >= len(path):
                    if path:
                        phase = "move_player"
                        move_idx = 0
                        snap_to_start()
                        self.player.state = "run"
                    else:
                        phase = "idle"

            elif phase == "move_player":
                move_timer += dt
                if move_timer >= MOVE_INTERVAL and move_idx < len(path):
                    r, c = path[move_idx]
                    self.player.rect.center = (c * TILE_SIZE + self.map_offset[0] + TILE_SIZE // 2,
                                               r * TILE_SIZE + self.map_offset[1] + TILE_SIZE // 2)
                    move_idx += 1
                    move_timer -= MOVE_INTERVAL
                if move_idx >= len(path):
                    phase = "idle"
                    self.player.state = "idle"

            # --- Draw Scene ---
            self.surface.blit(self.bg, (0, 0))
            self.map_model.update(dt)
            self.map_model.draw(self.surface)
            if visible_visited:
                self.draw_cells(visible_visited, (255, 255, 0, 80))
            if visible_path:
                self.draw_cells(visible_path, (0, 200, 255, 100))
            self.player_group.update(dt, self.map_model.collision_matrix)
            self.player_group.draw(self.surface)

            getattr(self.particles, f"{self.effect}Effect", self.particles.sandstormEffect)(self.surface)

            # --- Panel thông tin ---
            self.ui.draw_panel(self.surface, 1020, 30, 420, 700, title="INFORMATION PANEL")
            self.alg_panel.draw(self.surface, 1080, 380, 300, 200, mouse_pos, mouse_click)
            selected_alg = self.alg_panel.get_selected()

            # --- Nút phụ ---
            self.font_text = pygame.font.Font("Resources/Font/pixel2.ttf", 16)
            uitext = UIManager(self.font_text)
            if uitext.draw_image_button(self.surface, 1180, 630,
                                         self.imgNormal, self.imgHover, self.imgPressed,
                                         mouse_pos, mouse_click, 0.5, 0.7, text="Detail"):
                if search:
                    self.path_panel.toggle(self.map_model, path, search.thong_so(), selected_alg)

            if uitext.draw_image_button(self.surface, 1050, 630,
                                         self.imgNormal, self.imgHover, self.imgPressed,
                                         mouse_pos, mouse_click, 0.5, 0.7, text="History"):
                self.history_panel.toggle()

            if uitext.draw_image_button(self.surface, 1310, 630,
                                         self.imgNormal, self.imgHover, self.imgPressed,
                                         mouse_pos, mouse_click, 0.5, 0.7, text="Chart"):
                self.chart_panel.toggle(self.solve_history)

            # --- BACK ---
            if uitext.draw_image_button(self.surface, 0, 0,
                                         self.imgNormal_back, self.imgHover_back, self.imgPressed,
                                         mouse_pos, mouse_click, 1, 1):
                return "BACK"

            # --- Khi chọn thuật toán ---
            if selected_alg:
                if selected_alg in ["BFS", "DFS"]:
                    search = UninformedSearch(self.map_model, start, goal)
                    visited_states, path = getattr(search, selected_alg)()
                elif selected_alg in ["Greedy", "A*"]:
                    search = InformedSearch(self.map_model, start, goal)
                    visited_states, path = (search.Greedy() if selected_alg == "Greedy" else search.Astar())
                elif selected_alg in ["Beam", "SA"]:
                    search = LocalSearch(self.map_model, start, goal)
                    visited_states, path = (search.BeamSearch() if selected_alg == "Beam"
                                            else search.SimulatedAnnealingSearch())
                elif selected_alg == "NoOBS":
                    matrix = self.map_model.collision_matrix
                    starts = find_start_beliefs(matrix, 3)
                    goals = find_goal_beliefs(matrix, 3)
                    search = NOOBS(matrix, starts, goals)
                    belief_path = search.search()
                    visited_states = [list(b) for b in belief_path] if belief_path else []
                    path = []  # không có đường đi cụ thể cho player

                # --- Lưu vào lịch sử ---
                if search:
                    self.solve_history.append({
                        "algorithm": selected_alg,
                        **search.thong_so()
                    })

                visible_visited.clear()
                visible_path.clear()
                v_ptr = p_ptr = 0
                phase = "show_visited"
                snap_to_start()
                self.alg_panel.selected = None

            # --- Hiển thị thông tin ---
            if search:
                y = 120
                for k, v in search.thong_so().items():
                    self.ui.draw_text(self.surface, f"{k} {v}", 1080, y,
                                      (0, 0, 0), pathFont="Resources/Font/viethoa2.otf", size=20)
                    y += 40

            # --- Overlay panels ---
            self.history_panel.draw(self.surface, self.solve_history, mouse_pos, mouse_click)
            self.path_panel.draw(self.surface, mouse_pos, mouse_click)
            self.chart_panel.draw(self.surface, mouse_pos, mouse_click)

            pygame.display.flip()


# ============================================================
def main():
    pygame.init()
    screen = pygame.display.set_mode(RES)
    pygame.display.set_caption("MAZE")

    selected_config = {
        "background": "Resources/Maps/Background/Desert.png",
        "map": "Resources/Maps/Map1.tmx",
        "player": {
            "idle": ("Resources/Characters/idle_torchman.png", 96, 96, 6),
            "run": ("Resources/Characters/run_torchman.png", 96, 96, 6)
        },
        "effect": "baocat"
    }

    while True:
        menu = Menu(screen)
        choice = menu.run()

        if choice == "QUIT":
            pygame.quit()
            sys.exit()
        elif choice == "START GAME":
            app = App(selected_config)
            result = app.run()
            if result == "BACK":
                continue
        elif choice == "OPTIONS":
            options = Options(screen)
            selected_config = options.run()
            continue


if __name__ == "__main__":
    main()
