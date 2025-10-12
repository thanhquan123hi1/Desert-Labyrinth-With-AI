import pygame
from ui import UIManager

class AlgorithmPanel:
    def __init__(self):
        self.ui = UIManager()
        self.font = pygame.font.Font("Resources/Font/pixel1.ttf", 22)

        # --- Nút mũi tên ---
        self.imgNormal = pygame.image.load("Resources/Menu/buttons/arrnor.png").convert_alpha()
        self.imgHover = pygame.image.load("Resources/Menu/buttons/arrhover.png").convert_alpha()
        self.imgPressed = pygame.image.load("Resources/Menu/buttons/arrpressed.png").convert_alpha()

        # --- Các nhóm thuật toán ---
        self.groups = [
            {"name": "Uninformed Search", "algs": ["BFS", "DFS"]},
            {"name": "Informed Search", "algs": ["Greedy", "A*"]},
            {"name": "Local Search", "algs": ["Beam", "SA"]},
            {"name": "Belief Search", "algs": ["NoOBS"]},  
        ]
        self.index = 0
        self.selected = None  # thuật toán hiện chọn

    # -----------------------------------------------------
    def draw(self, surface, x, y, width=420, height=300, mouse_pos=(0, 0), mouse_click=False):
        """Vẽ panel nhóm thuật toán (tông parchment vàng-nâu, bo góc)."""

        # --- Panel parchment ---
        panel_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # Màu be vàng trong suốt, hợp background parchment
        pygame.draw.rect(panel_surface, (235, 205, 150, 160), panel_surface.get_rect(), border_radius=20)

        # Viền nâu nhẹ cho cảm giác da cũ
        pygame.draw.rect(panel_surface, (120, 80, 40, 200), panel_surface.get_rect(), 3, border_radius=20)

        surface.blit(panel_surface, (x, y))

        # --- Tiêu đề nhóm ---
        group = self.groups[self.index]
        title = self.font.render(group["name"], False, (60, 40, 10))  # nâu đậm, dễ đọc
        title_rect = title.get_rect(center=(x + width // 2, y + 25))
        surface.blit(title, title_rect)

        # --- Nút mũi tên trái/phải ---
        left_x = x + 35
        right_x = x + width - 67
        btn_y = y + height // 2 - 5

        if self.ui.draw_image_button(surface, left_x, btn_y,
                                     pygame.transform.flip(self.imgNormal, True, False),
                                     pygame.transform.flip(self.imgHover, True, False),
                                     pygame.transform.flip(self.imgPressed, True, False),
                                     mouse_pos, mouse_click, 0.25, 0.25):
            self.index = (self.index - 1) % len(self.groups)

        if self.ui.draw_image_button(surface, right_x, btn_y,
                                     self.imgNormal, self.imgHover, self.imgPressed,
                                     mouse_pos, mouse_click, 0.25, 0.25):
            self.index = (self.index + 1) % len(self.groups)

        # --- Vẽ danh sách thuật toán ---
        btn_w, btn_h = 150, 45
        start_x = x + width // 2 - btn_w // 2
        start_y = y + 60

        for i, alg in enumerate(group["algs"]):
            rect_y = start_y + i * (btn_h + 20)
            btn_rect = pygame.Rect(start_x, rect_y, btn_w, btn_h)

            # Hover / click / selected
            hovered = btn_rect.collidepoint(mouse_pos)
            if self.selected == alg:
                base_color = (200, 150, 80, 180)     # vàng nâu đậm hơn khi được chọn
                border_color = (100, 60, 20, 220)
                text_color = (20, 10, 0)
            elif hovered:
                base_color = (255, 220, 150, 190)    # sáng hơn khi hover
                border_color = (120, 80, 40, 220)
                text_color = (30, 20, 5)
            else:
                base_color = (240, 210, 160, 160)    # vàng be nhạt bình thường
                border_color = (100, 70, 30, 180)
                text_color = (70, 50, 20)

            # Bo góc
            btn_surface = pygame.Surface((btn_w, btn_h), pygame.SRCALPHA)
            pygame.draw.rect(btn_surface, base_color, (0, 0, btn_w, btn_h), border_radius=10)
            pygame.draw.rect(btn_surface, border_color, (0, 0, btn_w, btn_h), 2, border_radius=10)
            surface.blit(btn_surface, (start_x, rect_y))

            # Vẽ chữ
            txt = self.font.render(alg, False, text_color)
            txt_rect = txt.get_rect(center=btn_rect.center)
            surface.blit(txt, txt_rect)

            # Click chọn
            if mouse_click and hovered:
                self.selected = alg

    # -----------------------------------------------------
    def get_selected(self):
        """Trả về tên thuật toán đang chọn"""
        return self.selected

    def get_group_name(self):
        """Trả về tên nhóm hiện tại"""
        return self.groups[self.index]["name"]
