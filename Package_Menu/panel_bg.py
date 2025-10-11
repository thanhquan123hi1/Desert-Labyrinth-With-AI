import pygame
import os
from ui import UIManager
from settings import RES

class BGPanel:
    def __init__(self, backgrounds, font_path="Resources/Font/pixel1.ttf"):
        """
        backgrounds: danh sách đường dẫn tới các file background thật (ảnh lớn)
        """
        # Ảnh khung panel nền
        self.panel_img = pygame.image.load("Resources/Menu/khunggo.png").convert_alpha()

        # Danh sách background gốc (ảnh lớn)
        self.backgrounds = backgrounds

        # Tạo danh sách thumbnail preview tự động
        self.previews = []
        for bg_path in backgrounds:
            if os.path.exists(bg_path):
                img = pygame.image.load(bg_path).convert()
                thumb = pygame.transform.smoothscale(img, (220, 140))
                self.previews.append(thumb)
            else:
                placeholder = pygame.Surface((220, 140))
                placeholder.fill((100, 100, 100))
                self.previews.append(placeholder)

        # Font chữ tiêu đề
        self.font = pygame.font.Font(font_path, 20)

        # 3 trạng thái nút mũi tên (normal / hover / pressed)
        self.imgNormal = pygame.image.load("Resources/Menu/buttons/arrnor.png").convert_alpha()
        self.imgHover = pygame.image.load("Resources/Menu/buttons/arrhover.png").convert_alpha()
        self.imgPressed = pygame.image.load("Resources/Menu/buttons/arrpressed.png").convert_alpha()

        # UI Manager để vẽ nút
        self.ui = UIManager()

        # Chỉ số đang chọn
        self.index = 0

        # --- Hiệu ứng chuyển nền ---
        self.transitioning = False
        self.transition_alpha = 0
        self.transition_speed = 10  # tốc độ fade
        self.old_bg = None
        self.new_bg = pygame.image.load(self.backgrounds[self.index]).convert()
        self.new_bg = pygame.transform.smoothscale(self.new_bg, RES)

    # -----------------------------------------------------------------
    def draw(self, surface, x, y, width=360, height=450, mouse_pos=(0,0), mouse_click=False):
        """Vẽ panel chọn background"""
        # --- Vẽ khung panel ---
        panel_scaled = pygame.transform.smoothscale(self.panel_img, (width, height))
        surface.blit(panel_scaled, (x, y))

        # --- Tiêu đề ---
        bg_name = os.path.basename(self.backgrounds[self.index]).split(".")[0]
        title = self.font.render(f"Background: {bg_name}", False, (255, 255, 255))
        title_rect = title.get_rect(center=(x + width // 2, y + 47))
        surface.blit(title, title_rect)

        # --- Ảnh preview ---
        preview_img = self.previews[self.index]
        preview_rect = preview_img.get_rect(center=(x + width // 2, y + height // 2 + 15))
        surface.blit(preview_img, preview_rect)

        # --- Nút trái/phải ---
        left_x = x + 35
        right_x = x + width - 67
        btn_y = y + height // 2 - 5

        changed = False 

        # Nút trái
        if self.ui.draw_image_button(
            surface, left_x, btn_y,
            pygame.transform.flip(self.imgNormal, True, False),
            pygame.transform.flip(self.imgHover, True, False),
            pygame.transform.flip(self.imgPressed, True, False),
            mouse_pos, mouse_click, 0.25, 0.25
        ):
            old_index = self.index
            self.index = (self.index - 1) % len(self.backgrounds)
            changed = (self.index != old_index)

        # Nút phải
        if self.ui.draw_image_button(
            surface, right_x, btn_y,
            self.imgNormal, self.imgHover, self.imgPressed,
            mouse_pos, mouse_click, 0.25, 0.25
        ):
            old_index = self.index
            self.index = (self.index + 1) % len(self.backgrounds)
            changed = (self.index != old_index)

        # --- Bắt đầu hiệu ứng chuyển nền nếu có thay đổi ---
        if changed:
            self.start_transition()

    # -----------------------------------------------------------------
    def start_transition(self):
        """Bắt đầu hiệu ứng fade giữa 2 background"""
        self.transitioning = True
        self.transition_alpha = 0
        self.old_bg = self.new_bg.copy()
        self.new_bg = pygame.image.load(self.backgrounds[self.index]).convert()
        self.new_bg = pygame.transform.smoothscale(self.new_bg, RES)

    # -----------------------------------------------------------------
    def update_background(self, surface):
        """Cập nhật và vẽ hiệu ứng chuyển nền (fade mượt)"""
        if not self.transitioning:
            surface.blit(self.new_bg, (0, 0))
            return

        # Tăng alpha để hòa trộn dần giữa 2 ảnh
        self.transition_alpha += self.transition_speed
        if self.transition_alpha >= 255:
            self.transitioning = False
            surface.blit(self.new_bg, (0, 0))
            return

        # Blend giữa 2 ảnh
        old_surf = self.old_bg.copy()
        new_surf = self.new_bg.copy()

        # Tạo surface trung gian
        blend = pygame.Surface(RES, pygame.SRCALPHA)
        old_surf.set_alpha(255 - self.transition_alpha)
        new_surf.set_alpha(self.transition_alpha)
        blend.blit(old_surf, (0, 0))
        blend.blit(new_surf, (0, 0))
        surface.blit(blend, (0, 0))

    # -----------------------------------------------------------------
    def get_selected(self):
        """Trả về đường dẫn background đang chọn"""
        return self.backgrounds[self.index]
