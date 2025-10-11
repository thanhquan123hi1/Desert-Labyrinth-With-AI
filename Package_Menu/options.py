import pygame, sys
from Package_Animation import SpriteSheetAnimation
from ui import UIManager
from .panel_effects import EffectPanel
from .panel_bg import BGPanel
from .panel_player import PlayerPanel
from .panel_map import MapPanel    
from Package_Animation import Particles


class Options:
    def __init__(self, screen):
        self.screen = screen
        self.ui = UIManager()
        self.clock = pygame.time.Clock()

        self.backgrounds = [
            "Resources/Maps/Background/Desert.png",
            "Resources/Maps/Background/Tuyet1.png",
            "Resources/Maps/Background/Tuyet2.png",
            "Resources/Maps/Background/Tuyet3.png",
            "Resources/Maps/Background/Tuyet4.png",
            "Resources/Maps/Background/Forest.png",
            "Resources/Maps/Background/Jungle.png",
            "Resources/Maps/Background/Cave.png",
            "Resources/Maps/Background/Dungeon.png",
        ]
        self.maps = [
            "Resources/Maps/Map1.tmx",
            "Resources/Maps/Map2.tmx",
            "Resources/Maps/Map3.tmx",
            "Resources/Maps/Map4.tmx",
            "Resources/Maps/Map5.tmx",
        ]
        self.map_previews = [
            "Resources/Maps/Maze1.png",
            "Resources/Maps/Maze2.png",
            "Resources/Maps/Maze3.png",
            "Resources/Maps/Maze4.png",
            "Resources/Maps/Maze5.png"
        ]
        self.players = [
            {
                "idle": ("Resources/Characters/idle_torchman.png", 96, 96, 6),
                "run":  ("Resources/Characters/run_torchman.png", 96, 96, 6)
            },
            {
                "idle": ("Resources/Characters/idle_blue.png", 96, 96, 6),
                "run":  ("Resources/Characters/run_blue.png", 96, 96, 6)
            },
            {
                "idle": ("Resources/Characters/idle_yellow.png", 96, 96, 6),
                "run":  ("Resources/Characters/run_yellow.png", 96, 96, 6)
            },
            {
                "idle": ("Resources/Characters/idle_red.png", 96, 96, 6),
                "run":  ("Resources/Characters/run_red.png", 96, 96, 6)
            },
        ]

        # --- Các panel ---
        self.bg_panel = BGPanel(self.backgrounds)
        self.map_panel = MapPanel(self.maps, self.map_previews)  
        self.player_panel = PlayerPanel(self.players)
        self.effect_panel = EffectPanel()

        self.particles = Particles()
        self.current_effect = "baocat"


        # --- Nút Back ---
        self.imgNormal_back = pygame.image.load("Resources/Maps/buttons/back_normal.png").convert_alpha()
        self.imgHover_back = pygame.image.load("Resources/Maps/buttons/back_hover.png").convert_alpha()
        self.imgPressed_back = pygame.image.load("Resources/Maps/buttons/back_pressed.png").convert_alpha()

        # --- Chỉ số mặc định ---
        self.bg_index = 0
        self.map_index = 0
        self.player_index = 0


    # ------------------------------------------------------------
    def run(self):
        """Vòng lặp chính của màn hình Options"""
        while True:
            dt = self.clock.tick(60) / 1000
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_click = True

            # Cập nhật và vẽ hiệu ứng chuyển nền (fade mượt)
            self.bg_panel.update_background(self.screen)


            # --- Panel Background (trái - giữ nguyên) ---
            self.bg_panel.draw(
                self.screen,
                x=5, y=300, width=350, height=250,
                mouse_pos=mouse_pos, mouse_click=mouse_click
            )

            # --- Panel Map (giữa - mới thêm, cùng kích thước) ---
            self.map_panel.draw(
                self.screen,
                x=410, y=50, width=600, height=400,
                mouse_pos=mouse_pos, mouse_click=mouse_click
            )

            # --- Panel Player (phải - giữ nguyên) ---
            self.player_panel.draw(
                self.screen,
                x=1100, y=300, width=350, height=250,
                mouse_pos=mouse_pos, mouse_click=mouse_click,
                dt=dt
            )

            # --- Panel Hiệu ứng (giữ nguyên) ---
            self.effect_panel.draw(
                self.screen, 470, 600, 500, 150,
                mouse_pos, mouse_click,
                icon_size=(60, 60),
                spacing_x=10, offset_y=15, offset_x=45
            )

            # --- Cập nhật hiệu ứng môi trường ---
            selected_effect = self.effect_panel.get_selected()
            if selected_effect != self.current_effect:
                self.current_effect = selected_effect
                self.particles.reset_particles()

            if self.current_effect == "baocat":
                self.particles.sandstormEffect(self.screen)
            elif self.current_effect == "domdom":
                self.particles.firefliesEffect(self.screen)
            elif self.current_effect == "leaves":
                self.particles.leavesEffect(self.screen)
            elif self.current_effect == "rain":
                self.particles.rainEffect(self.screen)
            elif self.current_effect == "snow":
                self.particles.snowEffect(self.screen)

            # --- Nút BACK ---
            if self.ui.draw_image_button(self.screen, 0, 0,
                                         self.imgNormal_back, self.imgHover_back, self.imgPressed_back,
                                         mouse_pos, mouse_click, 1.1, 1.1):
                return self.get_selected_options()


            pygame.display.flip()

    # ------------------------------------------------------------
    def get_selected_options(self):
        return {
            "background": self.bg_panel.get_selected(),
            "map": self.map_panel.get_selected(),    
            "player": self.player_panel.get_selected(),
            "effect": self.effect_panel.get_selected()
        }
