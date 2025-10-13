import pygame

class EffectPanel:
    def __init__(self):
        self.panel_img = pygame.image.load("Resources/Menu/envir.png").convert_alpha()

        self.original_effects = [
            pygame.image.load("Resources/Menu/envir/baocat.png").convert_alpha(),
            pygame.image.load("Resources/Menu/envir/fireflies.png").convert_alpha(),
            pygame.image.load("Resources/Menu/envir/leaves.png").convert_alpha(),
            pygame.image.load("Resources/Menu/envir/rain.png").convert_alpha(),
            pygame.image.load("Resources/Menu/envir/snow.png").convert_alpha(),
        ]

        # Tên hiệu ứng tương ứng
        self.effect_names = ["baocat", "fireflies", "leaves", "rain", "snow"]

        # Kích thước icon mặc định
        self.icon_size = (90, 90)
        self.effects = [pygame.transform.smoothscale(img, self.icon_size) for img in self.original_effects]

        # Hiệu ứng đang được chọn
        self.selected = 0

        # Màu nền khi hover
        self.hover_color = (255, 255, 200, 70)

    # ---------------------------------------------------------------------
    def set_icon_size(self, size):
        """Thay đổi kích thước icon (tuple width, height)"""
        self.icon_size = size
        self.effects = [pygame.transform.smoothscale(img, self.icon_size) for img in self.original_effects]

    # ---------------------------------------------------------------------
    def draw(
        self,
        surface,
        x, y, width, height,
        mouse_pos, mouse_click,
        icon_size=None,
        spacing_x=None,
        offset_x=None,
        offset_y=None
    ):
        """
        Vẽ panel hiệu ứng tại vị trí (x, y) với kích thước width, height.
        - icon_size: (w, h) — kích thước icon, có thể None (mặc định 90x90)
        - spacing_x: khoảng cách giữa các icon (pixel), nếu None sẽ tự canh đều
        - offset_x: dịch chuyển tất cả icon theo trục X (âm sang trái, dương sang phải)
        - offset_y: dịch chuyển tất cả icon theo trục Y (âm lên, dương xuống)
        """
        # --- Cập nhật kích thước icon nếu có truyền vào ---
        if icon_size is not None:
            self.set_icon_size(icon_size)

        # --- Vẽ panel nền ---
        panel_scaled = pygame.transform.smoothscale(self.panel_img, (width, height))
        surface.blit(panel_scaled, (x, y))

        # --- Tính toán bố cục icon ---
        total_icons = len(self.effects)
        icon_w, icon_h = self.icon_size

        # khoảng cách giữa các icon (nếu không truyền thì tự canh đều)
        if spacing_x is None:
            available_width = width - 2 * 40
            total_icons_width = total_icons * icon_w
            total_spacing = max(0, available_width - total_icons_width)
            spacing_x = total_spacing / (total_icons - 1) if total_icons > 1 else 0

        # vị trí trung tâm (có thể chỉnh offset)
        offset_x = offset_x or 0
        offset_y = offset_y or 0
        base_x = x + 40 + offset_x
        center_y = y + height // 2 + offset_y

        for i, icon in enumerate(self.effects):
            icon_x = base_x + i * (icon_w + spacing_x)
            rect = icon.get_rect(center=(icon_x + icon_w // 2, center_y))

            # --- Hover highlight ---
            if rect.collidepoint(mouse_pos):
                hover_surf = pygame.Surface((rect.width + 12, rect.height + 12), pygame.SRCALPHA)
                hover_surf.fill(self.hover_color)
                surface.blit(hover_surf, (rect.x - 6, rect.y - 6))

            # --- Vẽ icon ---
            surface.blit(icon, rect)

            # --- Viền vàng nếu được chọn ---
            if i == self.selected:
                pygame.draw.rect(surface, (255, 255, 0), rect.inflate(12, 12), 4)

            # --- Click chọn hiệu ứng ---
            if mouse_click and rect.collidepoint(mouse_pos):
                self.selected = i

    # ---------------------------------------------------------------------
    def get_selected(self):
        """Trả về tên hiệu ứng đang chọn"""
        return self.effect_names[self.selected]
