import pygame, os
from ui import UIManager

class MapPanel:
    def __init__(self, maps, map_previews, font_path="Resources/Font/pixel1.ttf"):
        """
        maps          : danh sách đường dẫn .tmx của các bản đồ
        map_previews  : danh sách đường dẫn hình thumbnail tương ứng
        """
        # --- Ảnh khung panel ---
        self.panel_img = pygame.image.load("Resources/Menu/khungda.png").convert_alpha()

        # --- Dữ liệu ---
        self.maps = maps
        self.map_previews = map_previews
        self.font = pygame.font.Font(font_path, 22)

        # --- UI ---
        self.ui = UIManager()

        # --- Nút mũi tên ---
        self.imgNormal = pygame.image.load("Resources/Menu/buttons/arrnor.png").convert_alpha()
        self.imgHover = pygame.image.load("Resources/Menu/buttons/arrhover.png").convert_alpha()
        self.imgPressed = pygame.image.load("Resources/Menu/buttons/arrpressed.png").convert_alpha()

        # --- Chỉ số hiện tại ---
        self.index = 0

        # --- Danh sách preview (ảnh thu nhỏ) ---
        self.previews = []
        for path in self.map_previews:
            if os.path.exists(path):
                img = pygame.image.load(path).convert()
                # Scale ảnh để vừa với panel (giữ tỉ lệ 220x140)
                thumb = pygame.transform.smoothscale(img, (220, 140))  
                self.previews.append(thumb)
            else:
                # Ảnh placeholder nếu thiếu file
                placeholder = pygame.Surface((220, 140))
                placeholder.fill((80, 80, 80))
                self.previews.append(placeholder)

    # -----------------------------------------------------------------
    def draw(self, surface, x, y, width=600, height=400, mouse_pos=(0,0), mouse_click=False):
        """Vẽ panel chọn map (không hiệu ứng chuyển cảnh)"""
        # --- Panel nền ---
        panel_scaled = pygame.transform.scale(self.panel_img, (width, height))
        surface.blit(panel_scaled, (x, y))

        # --- Ảnh preview (scale cho phù hợp khung) ---
        preview = self.previews[self.index]
        # Scale lại ảnh cho cân đối trong khung panel
        preview_scaled = pygame.transform.scale(preview, (440, 290))  
        preview_rect = preview_scaled.get_rect(center=(x + width // 2 + 5, y + height // 2 + 5))
        surface.blit(preview_scaled, preview_rect)

        # --- Nút trái/phải ---
        left_x = x + 35
        right_x = x + width - 67
        btn_y = y + height // 2 - 5

        # Nút trái
        if self.ui.draw_image_button(
            surface, left_x, btn_y,
            pygame.transform.flip(self.imgNormal, True, False),
            pygame.transform.flip(self.imgHover, True, False),
            pygame.transform.flip(self.imgPressed, True, False),
            mouse_pos, mouse_click, 0.25, 0.25
        ):
            self.index = (self.index - 1) % len(self.maps)

        # Nút phải
        if self.ui.draw_image_button(
            surface, right_x, btn_y,
            self.imgNormal, self.imgHover, self.imgPressed,
            mouse_pos, mouse_click, 0.25, 0.25
        ):
            self.index = (self.index + 1) % len(self.maps)

    # -----------------------------------------------------------------
    def get_selected(self):
        """Trả về map được chọn"""
        return self.maps[self.index]
