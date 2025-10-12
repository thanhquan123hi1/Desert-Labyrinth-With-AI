import pygame
import sys
import numpy as np

from settings import RES, TILE_SIZE
from map_model import MapModel
from player import Player
from ui import UIManager
from Package_Menu import Menu, Options
from Package_Panel import SolveHistoryPanel, PathViewPanel, ChartPanel
from Package_Animation import Particles
from Package_Algorithm import AlgorithmPanel
from Package_Core import AlgorithmManager, GameRenderer


# ============================================================
class App:
    def __init__(self, config):
        pygame.init()
        self.surface = pygame.display.set_mode(RES)
        pygame.display.set_caption("MAZE")
        self.clock = pygame.time.Clock()
        
        self.history = []

        # --- Background ---
        self.bg = pygame.image.load(config["background"]).convert()
        self.bg = pygame.transform.scale(self.bg, RES)

        # --- Map ---
        self.map_offset = (32, 32)
        self.map_model = MapModel(config["map"], offset=self.map_offset)

        # --- Player ---
        self.player_group = pygame.sprite.Group()
        self.player = Player(
            (self.map_offset[0] + 32, self.map_offset[1] + 32),
            self.player_group,
            sprite_idle=config["player"]["idle"],
            sprite_run=config["player"]["run"],
            offset=self.map_offset
        )

        # --- Goal (tọa độ đích) ---
        self.goal = config.get("goal", (19, 28))

        # --- Hiệu ứng môi trường ---
        self.particles = Particles()
        self.effect = config.get("effect", "baocat")

        # --- Core Managers ---
        self.alg_manager = AlgorithmManager(self.map_model)
        self.renderer = GameRenderer(
            self.surface, self.map_model, self.player, self.goal,
            self.map_offset, self.particles, self.effect
        )

        # --- UI ---
        self.ui = UIManager()

        # --- Hiệu ứng môi trường ---
        self.particles = Particles()
        self.effect = config.get("effect", "baocat")

        # --- Buttons ---
        self.imgNormal = pygame.image.load("Resources/Menu/buttons/btn_bhover.png").convert_alpha()
        self.imgHover = pygame.image.load("Resources/Menu/buttons/btn_yhover.png").convert_alpha()
        self.imgPressed = pygame.image.load("Resources/Menu/buttons/btn_bpressed.png").convert_alpha()

        self.imgNormal_back = pygame.image.load("Resources/Maps/buttons/back_normal.png").convert_alpha()
        self.imgHover_back = pygame.image.load("Resources/Maps/buttons/back_hover.png").convert_alpha()
        self.imgPressed_back = pygame.image.load("Resources/Maps/buttons/back_pressed.png").convert_alpha()

        # --- Panels ---
        self.alg_panel = AlgorithmPanel()
        self.solve_history = []
        self.history_panel = SolveHistoryPanel()
        self.path_panel = PathViewPanel()
        self.chart_panel = ChartPanel()

    # ----------------------------------------------------------
    def run(self):
        """Vòng lặp chính của màn chơi."""
        start = (int((self.player.rect.centery - self.map_offset[1]) // TILE_SIZE),
                 int((self.player.rect.centerx - self.map_offset[0]) // TILE_SIZE))
        print(f"Start: {start}, Goal: {self.goal}")

        visited_states, path = [], []
        visible_visited, visible_path = [], []
        phase = "idle"

        v_ptr = p_ptr = move_idx = 0
        visited_timer = path_timer = move_timer = 0.0
        VISITED_INTERVAL, PATH_INTERVAL, MOVE_INTERVAL = 0.02, 0.05, 0.05

        def snap_to_start():
            sr, sc = start
            self.player.rect.center = (
                sc * TILE_SIZE + self.map_offset[0] + TILE_SIZE // 2,
                sr * TILE_SIZE + self.map_offset[1] + TILE_SIZE // 2
            )

        # =====================================================
        while True:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False

            # --- Event ---
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    mouse_click = True
                self.history_panel.handle_event(e)
                self.path_panel.handle_event(e)

            dt = self.clock.tick(60) / 1000.0

            # --- Cập nhật hiệu ứng từng giai đoạn ---
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
                if move_idx < len(path) - 1:
                    start_r, start_c = path[move_idx]
                    end_r, end_c = path[move_idx + 1]
                    start_pos = (
                        start_c * TILE_SIZE + self.map_offset[0] + TILE_SIZE // 2,
                        start_r * TILE_SIZE + self.map_offset[1] + TILE_SIZE // 2
                    )
                    end_pos = (
                        end_c * TILE_SIZE + self.map_offset[0] + TILE_SIZE // 2,
                        end_r * TILE_SIZE + self.map_offset[1] + TILE_SIZE // 2
                    )

                    move_timer += dt
                    t = min(move_timer / MOVE_INTERVAL, 1.0)
                    lerp = lambda a, b, t: a + (b - a) * t
                    x = lerp(start_pos[0], end_pos[0], t)
                    y = lerp(start_pos[1], end_pos[1], t)
                    self.player.rect.center = (x, y)

                    # Khi hoàn tất một bước
                    if t >= 1.0:
                        move_idx += 1
                        move_timer = 0.0
                        self.particles.playerStepEffect(end_pos)
                else:
                    phase = "idle"
                    self.player.state = "idle"


            # =====================================================
            # --- Vẽ khung cảnh ---
            self.surface.blit(self.bg, (0, 0))
            self.renderer.draw(dt, visible_visited, visible_path)
            getattr(self.particles, f"{self.effect}Effect", self.particles.sandstormEffect)(self.surface)

            # --- Panel thông tin ---
            self.ui.draw_panel(self.surface, 1020, 30, 420, 700, title="INFORMATION PANEL")
            self.alg_panel.draw(self.surface, 1080, 380, 300, 200, mouse_pos, mouse_click)
            selected_alg = self.alg_panel.get_selected()

            # --- Nút phụ ---
            font_text = pygame.font.Font("Resources/Font/pixel2.ttf", 16)
            uitext = UIManager(font_text)

            # Button: DETAIL
            if uitext.draw_image_button(self.surface, 1180, 630,
                                        self.imgNormal, self.imgHover, self.imgPressed,
                                        mouse_pos, mouse_click, 0.5, 0.7, text="Detail"):
                search = self.alg_manager.search
                if search:
                    self.path_panel.toggle(
                        self.map_model,
                        path,
                        search.thong_so(),
                        self.alg_manager.selected_alg,
                        getattr(search, "starts", getattr(search, "start", None)),
                        getattr(search, "goals", getattr(search, "goal", None))
                    )
            # Button: HISTORY
            if uitext.draw_image_button(self.surface, 1050, 630,
                                        self.imgNormal, self.imgHover, self.imgPressed,
                                        mouse_pos, mouse_click, 0.5, 0.7, text="History"):
                self.history_panel.toggle()

            # Button: CHART
            if uitext.draw_image_button(self.surface, 1310, 630,
                                        self.imgNormal, self.imgHover, self.imgPressed,
                                        mouse_pos, mouse_click, 0.5, 0.7, text="Chart"):
                self.chart_panel.toggle(self.solve_history)

            # Button: BACK
            if uitext.draw_image_button(self.surface, 0, 0,
                                        self.imgNormal_back, self.imgHover_back, self.imgPressed,
                                        mouse_pos, mouse_click, 1, 1):
                return "BACK"

            # =====================================================
            # --- Khi chọn thuật toán ---
            if selected_alg:
                search, visited_states, path, info = self.alg_manager.run_algorithm(selected_alg, start, self.goal)
                # Reset hiệu ứng trước khi hiển thị kết quả mới
                self.renderer.reset_effects()
                if selected_alg == "NoOBS" and hasattr(search, "goals"):
                    self.renderer.goals = list(search.goals)
                else:
                    self.renderer.goals = [self.goal]

                if search:
                    self.solve_history.append({   # <<< đổi từ self.history → self.solve_history
                        "algorithm": selected_alg,
                        **info
                    })

                visible_visited.clear()
                visible_path.clear()
                v_ptr = p_ptr = 0
                phase = "show_visited"
                snap_to_start()
                self.alg_panel.selected = None

            # --- Hiển thị thông tin thuật toán ---
            search_info = self.alg_manager.get_info()
            if search_info:
                y = 120
                for k, v in search_info.items():
                    text = f"{k} {v}"

                    # 🔹 Nếu là dòng "KẾT QUẢ"
                    if "KẾT QUẢ" in k.upper():
                        if str(v).lower() in ["fail", "thất bại"]:
                            color = (255, 60, 60)   # đỏ
                        else:
                            color = (10, 25, 60)     # xanh lá
                    else:
                        color = (0, 0, 0)           # đen mặc định

                    self.ui.draw_text(
                        self.surface,
                        text, 1080, y,
                        color,
                        pathFont="Resources/Font/viethoa2.otf",
                        size=20
                    )
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

    # --- Cấu hình mặc định ban đầu ---
    selected_config = {
        "background": "Resources/Maps/Background/Desert.png",
        "map": "Resources/Maps/Map1.tmx",
        "player": {
            "idle": ("Resources/Characters/idle_torchman.png", 96, 96, 6),
            "run": ("Resources/Characters/run_torchman.png", 96, 96, 6)
        },
        "effect": "baocat",
    }

    # --- Menu Loop ---
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
