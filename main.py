import pygame, sys
from settings import RES, TILE_SIZE
from map_model import MapModel
from player import Player
from ui import UIManager
from Package_Menu import Menu, Options
from Package_Algorithm import UninformedSearch, InformedSearch, LocalSearch, AlgorithmPanel
from Package_Animation import Particles


class App:
    def __init__(self, config):
        pygame.init()
        self.surface = pygame.display.set_mode(RES)

        # --- Background ---
        self.bg = pygame.image.load(config["background"]).convert()
        self.bg = pygame.transform.scale(self.bg, RES)
        pygame.display.set_caption("MAZE")
        self.clock = pygame.time.Clock()

        # --- Map offset ---
        self.map_offset = (32, 32)

        # --- Map ---
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

        # --- Nút hình ---
        self.imgNormal = pygame.image.load("Resources/Menu/buttons/Button_Blue.png").convert_alpha()
        self.imgHover = pygame.image.load("Resources/Menu/buttons/Button_Hover.png").convert_alpha()
        self.imgPressed = pygame.image.load("Resources/Menu/buttons/Button_Blue_Pressed.png").convert_alpha()

        # --- Back ---
        self.imgNormal_back = pygame.image.load("Resources/Maps/buttons/back_normal.png").convert_alpha()
        self.imgHover_back = pygame.image.load("Resources/Maps/buttons/back_hover.png").convert_alpha()
        self.imgPressed_back = pygame.image.load("Resources/Maps/buttons/back_pressed.png").convert_alpha()

        # --- Panel Thuật toán ---
        self.alg_panel = AlgorithmPanel()

    # ----------------------------------------------------------
    def draw_cells(self, cells, color_rgba):
        for (r, c) in cells:
            rect = pygame.Rect(
                c * TILE_SIZE + self.map_offset[0],
                r * TILE_SIZE + self.map_offset[1],
                TILE_SIZE, TILE_SIZE
            )
            s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            s.fill(color_rgba)
            self.surface.blit(s, rect.topleft)

    # ----------------------------------------------------------
    def run(self):
        start = (int((self.player.rect.centery - self.map_offset[1]) // TILE_SIZE),
                 int((self.player.rect.centerx - self.map_offset[0]) // TILE_SIZE))
        goal = (19, 28)
        print(f"Start: {start}, Goal: {goal}")

        phase = "idle"
        visited_states, path = [], []
        visible_visited, visible_path = [], []
        search = None

        # Timer
        v_ptr = p_ptr = move_idx = 0
        visited_timer = path_timer = move_timer = 0.0
        VISITED_INTERVAL = 0.02
        PATH_INTERVAL = 0.05
        MOVE_INTERVAL = 0.05

        def snap_player_to_start():
            sr, sc = start
            self.player.rect.centerx = sc * TILE_SIZE + self.map_offset[0] + TILE_SIZE // 2
            self.player.rect.centery = sr * TILE_SIZE + self.map_offset[1] + TILE_SIZE // 2

        # =====================================================
        while True:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_click = True

            dt = self.clock.tick(60) / 1000.0

            # ====== Animation thuật toán ======
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
                        snap_player_to_start()
                        self.player.state = "run"
                    else:
                        phase = "idle"

            elif phase == "move_player":
                move_timer += dt
                if move_timer >= MOVE_INTERVAL and move_idx < len(path):
                    r, c = path[move_idx]
                    if move_idx + 1 < len(path):
                        nr, nc = path[move_idx + 1]
                        self.player.facing_right = (nc > c)
                    self.player.rect.centerx = c * TILE_SIZE + self.map_offset[0] + TILE_SIZE // 2
                    self.player.rect.centery = r * TILE_SIZE + self.map_offset[1] + TILE_SIZE // 2
                    move_idx += 1
                    move_timer -= MOVE_INTERVAL
                if move_idx >= len(path):
                    phase = "idle"
                    self.player.state = "idle"

            # ====== Update logic ======
            if phase == "idle":
                self.player_group.update(dt, self.map_model.collision_matrix)
            self.map_model.update(dt)

            # ====== Vẽ nền và map ======
            self.surface.blit(self.bg, (0, 0))
            self.map_model.draw(self.surface)
            if visible_visited: self.draw_cells(visible_visited, (255, 255, 0, 80))
            if visible_path: self.draw_cells(visible_path, (0, 200, 255, 100))
            self.player_group.draw(self.surface)
            
            # ====== Panel thông tin ======
            self.ui.draw_panel(self.surface, 1020, 30, 420, 700, title="ALGORITHM PANEL")

            # --- Panel nhóm thuật toán ---
            self.alg_panel.draw(self.surface, 1080, 380, 300, 200, mouse_pos, mouse_click)
            selected_alg = self.alg_panel.get_selected()

            # ====== Hiệu ứng môi trường ======
            if self.effect == "baocat": self.particles.sandstormEffect(self.surface)
            elif self.effect == "domdom": self.particles.firefliesEffect(self.surface)
            elif self.effect == "leaves": self.particles.leavesEffect(self.surface)
            elif self.effect == "rain": self.particles.rainEffect(self.surface)
            elif self.effect == "snow": self.particles.snowEffect(self.surface)

            # --- Khi chọn thuật toán ---
            if selected_alg:
                if selected_alg in ["BFS", "DFS"]:
                    search = UninformedSearch(self.map_model, start, goal)
                    visited_states, path = getattr(search, selected_alg)()
                elif selected_alg in ["Greedy", "A*"]:
                    search = InformedSearch(self.map_model, start, goal)
                    if selected_alg == "Greedy":
                        visited_states, path = search.Greedy()
                    else:
                        visited_states, path = search.Astar()
                elif selected_alg in ["Beam", "SA"]:
                    search = LocalSearch(self.map_model, start, goal)
                    if selected_alg == "Beam":
                        visited_states, path = search.BeamSearch()
                    else:
                        visited_states, path = search.SimulatedAnnealingSearch()

                visible_visited.clear()
                visible_path.clear()
                v_ptr = p_ptr = 0
                visited_timer = path_timer = 0
                phase = "show_visited"
                snap_player_to_start()
                self.alg_panel.selected = None  # reset sau khi click

            # --- Nút BACK ---
            if self.ui.draw_image_button(self.surface, 0, 0,
                                         self.imgNormal_back, self.imgHover_back, self.imgPressed_back,
                                         mouse_pos, mouse_click, 1, 1):
                return "BACK"

            # --- Thông tin thuật toán ---
            if search and phase != "idle":
                info = search.thong_so()
                y = 120
                for k, v in info.items():
                    self.ui.draw_text(self.surface, f"{k} {v}", 1080, y,
                                      (0, 0, 0), pathFont="Resources/Font/viethoa2.otf", size=20)
                    y += 40
                if len(path) == 0:
                    self.ui.draw_text(self.surface, "Không tìm thấy đường!",
                                      1080, y + 10, (200, 0, 0),
                                      pathFont="Resources/Font/viethoa2.otf", size=20)

            pygame.display.flip()


# ============================================================
def main():
    pygame.init()
    screen = pygame.display.set_mode(RES)

    selected_config = {
        "background": "Resources/Maps/Background/Desert.png",
        "map": "Resources/Maps/Map1.tmx",
        "player": {
            "idle": ("Resources/Characters/idle_torchman.png", 96, 96, 6),
            "run":  ("Resources/Characters/run_torchman.png", 96, 96, 6)
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
            btn_choice = app.run()
            if btn_choice == "BACK":
                continue
        elif choice == "OPTIONS":
            options = Options(screen)
            selected_config = options.run()
            continue


# ============================================================
if __name__ == "__main__":
    main()
