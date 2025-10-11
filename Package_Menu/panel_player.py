import pygame, os
from ui import UIManager
from Package_Animation import SpriteSheetAnimation

class PlayerPanel:
    def __init__(self, players, font_path="Resources/Font/pixel1.ttf"):
        """
        players: danh sách dict chứa idle/run của các nhân vật
                 ví dụ:
                 [
                    {"idle": ("Resources/Characters/idle_torchman.png", 96, 96, 6),
                     "run":  ("Resources/Characters/run_torchman.png", 96, 96, 6)},
                    {"idle": ("Resources/Characters/idle_blue.png", 96, 96, 6),
                     "run":  ("Resources/Characters/run_blue.png", 96, 96, 6)},
                 ]
        """
        self.panel_img = pygame.image.load("Resources/Menu/khunggo.png").convert_alpha()
        self.players = players
        self.font = pygame.font.Font(font_path, 22)

        # Nút mũi tên
        self.imgNormal = pygame.image.load("Resources/Menu/buttons/arrnor.png").convert_alpha()
        self.imgHover = pygame.image.load("Resources/Menu/buttons/arrhover.png").convert_alpha()
        self.imgPressed = pygame.image.load("Resources/Menu/buttons/arrpressed.png").convert_alpha()

        self.ui = UIManager()
        self.index = 0  # player hiện tại

        # Tạo animation xem trước cho nhân vật đầu tiên
        self.player_idle_anim = self.create_idle_anim(self.players[self.index]["idle"])

    # -----------------------------------------------------------
    def create_idle_anim(self, idle_data):
        """Tạo animation từ dữ liệu idle (sprite sheet)."""
        path, fw, fh, count = idle_data
        return SpriteSheetAnimation(path, frame_width=fw, frame_height=fh, frame_count=count, fps=8, loop=True)

    # -----------------------------------------------------------
    def draw(self, surface, x, y, mouse_pos, mouse_click, dt, width=360, height=420):
        """Vẽ panel chọn player"""
        # --- Panel nền ---
        panel_scaled = pygame.transform.smoothscale(self.panel_img, (width, height))
        surface.blit(panel_scaled, (x, y))

        # --- Tiêu đề ---
        name = os.path.basename(self.players[self.index]["idle"][0]).split("_")[1].split(".")[0]
        title = self.font.render(f"Player: {name}", False, (255, 255, 255))
        title_rect = title.get_rect(center=(x + width // 2, y + 47))
        surface.blit(title, title_rect)

        # --- Vẽ animation xem trước ---
        self.player_idle_anim.update(dt)
        self.player_idle_anim.draw(surface, (x + width // 2, y + height // 2), scale=1.3)

        # --- Mũi tên trái/phải ---
        left_x = x + 35
        right_x = x + width - 67
        btn_y = y + height // 2 - 5

        # Nút trái
        if self.ui.draw_image_button(surface, left_x, btn_y,
                                     pygame.transform.flip(self.imgNormal, True, False),
                                     pygame.transform.flip(self.imgHover, True, False),
                                     pygame.transform.flip(self.imgPressed, True, False),
                                     mouse_pos, mouse_click, 0.25, 0.25):
            self.index = (self.index - 1) % len(self.players)
            self.player_idle_anim = self.create_idle_anim(self.players[self.index]["idle"])

        # Nút phải
        if self.ui.draw_image_button(surface, right_x, btn_y,
                                     self.imgNormal, self.imgHover, self.imgPressed,
                                     mouse_pos, mouse_click, 0.25, 0.25):
            self.index = (self.index + 1) % len(self.players)
            self.player_idle_anim = self.create_idle_anim(self.players[self.index]["idle"])

    # -----------------------------------------------------------
    def get_selected(self):
        """Trả về player hiện tại"""
        return self.players[self.index]
