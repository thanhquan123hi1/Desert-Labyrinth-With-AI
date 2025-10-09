import pygame, sys
from Package_Animation import SpriteSheetAnimation
from ui import UIManager

class Options:
    def __init__(self, screen):
        self.screen = screen
        self.ui = UIManager()
        self.clock = pygame.time.Clock()
        self.imgPanel = pygame.image.load("Resources/Menu/map_panel.png").convert_alpha()

        # back button
        self.imgNormal_back = pygame.image.load("Resources/Maps/buttons/back_normal.png").convert_alpha()
        self.imgHover_back = pygame.image.load("Resources/Maps/buttons/back_hover.png").convert_alpha()
        self.imgPressed_back = pygame.image.load("Resources/Maps/buttons/back_pressed.png").convert_alpha()

        # arrow animation (sheet)
        self.arrow_anim = SpriteSheetAnimation(
            "Resources/Animation/sheetarrow.png",
            frame_width=128,
            frame_height=128,
            frame_count=7,
            fps=15,
            loop=True
        )

        # --- Danh sách lựa chọn ---
        self.backgrounds = [
            "Resources/Maps/Background/Desert.png",
            "Resources/Maps/Background/Tuyet1.png",
            "Resources/Maps/Background/Tuyet2.png",
            "Resources/Maps/Background/Tuyet_4.png",
            "Resources/Maps/Background/Forest.png",
            "Resources/Maps/Background/jungle.png",
            "Resources/Maps/Background/cave.png",
            "Resources/Maps/Background/dungeon.png",
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

        # index mặc định
        self.bg_index = 0
        self.map_index = 0
        self.player_index = 0

        # tạo animation cho player idle ban đầu
        self.player_idle_anim = self.create_player_idle(self.players[self.player_index]["idle"])

    def create_player_idle(self, idle_data):
        path, fw, fh, count = idle_data
        return SpriteSheetAnimation(path, frame_width=fw, frame_height=fh, frame_count=count, fps=8, loop=True)

    def draw_preview(self, dt):
        # vẽ background (full screen)
        bg = pygame.image.load(self.backgrounds[self.bg_index]).convert()
        bg = pygame.transform.scale(bg, self.screen.get_size())
        self.screen.blit(bg, (0, 0))

        # panel khung preview
        self.ui.draw_panel(self.screen, 385, 50, 720, 550, img_panel=self.imgPanel)

        # vẽ map thumbnail
        map_preview = pygame.image.load(self.map_previews[self.map_index]).convert()
        map_preview = pygame.transform.scale(map_preview, (600, 420))
        self.screen.blit(map_preview, (450, 100))

        # update + draw player idle animation
        self.player_idle_anim.update(dt)
        self.player_idle_anim.draw(self.screen, (755, 650), scale=1.2)

    def draw_arrows(self, mouse_pos, mouse_click, dt):
        """Mũi tên chọn BG, MAP, PLAYER"""
        arrow_frames_right = self.arrow_anim.frames
        arrow_frames_left = [pygame.transform.flip(f, True, False) for f in self.arrow_anim.frames]

        # chọn background
        self.arrow_anim.update(dt)
        if self.arrow_anim.buttonSprite(self.screen, (30, 370), mouse_pos, mouse_click, scale=0.4, flip=True):
            self.bg_index = (self.bg_index - 1) % len(self.backgrounds)
        if self.arrow_anim.buttonSprite(self.screen, (1420, 370), mouse_pos, mouse_click, scale=0.4):
            self.bg_index = (self.bg_index + 1) % len(self.backgrounds)

        # chọn map
        if self.ui.draw_image_button(self.screen, 360, 310,
                                    arrow_frames_left[0], arrow_frames_left[3], arrow_frames_left[6],
                                    mouse_pos, mouse_click, 0.4, 0.4):
            self.map_index = (self.map_index - 1) % len(self.maps)

        if self.ui.draw_image_button(self.screen, 1080, 310,
                                    arrow_frames_right[0], arrow_frames_right[3], arrow_frames_right[6],
                                    mouse_pos, mouse_click, 0.4, 0.4):
            self.map_index = (self.map_index + 1) % len(self.maps)

        # chọn player
        if self.ui.draw_image_button(self.screen, 650, 660,
                                    arrow_frames_left[0], arrow_frames_left[3], arrow_frames_left[6],
                                    mouse_pos, mouse_click, 0.4, 0.4):
            self.player_index = (self.player_index - 1) % len(self.players)
            self.player_idle_anim = self.create_player_idle(self.players[self.player_index]["idle"])

        if self.ui.draw_image_button(self.screen, 808, 660,
                                    arrow_frames_right[0], arrow_frames_right[3], arrow_frames_right[6],
                                    mouse_pos, mouse_click, 0.4, 0.4):
            self.player_index = (self.player_index + 1) % len(self.players)
            self.player_idle_anim = self.create_player_idle(self.players[self.player_index]["idle"])

    def run(self):
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

            # preview
            self.draw_preview(dt)

            # arrows
            self.draw_arrows(mouse_pos, mouse_click, dt)

            # nút back
            if self.ui.draw_image_button(self.screen, 0, 0,
                                         self.imgNormal_back, self.imgHover_back, self.imgPressed_back,
                                         mouse_pos, mouse_click, 1.1, 1.1):
                return self.get_selected_options()

            pygame.display.flip()

    def get_selected_options(self):
        return {
            "background": self.backgrounds[self.bg_index],
            "map": self.maps[self.map_index],
            "player": self.players[self.player_index]
        }
