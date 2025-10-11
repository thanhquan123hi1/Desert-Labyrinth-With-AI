import pygame
from settings import RES
from ui import UIManager
import math


class SolveHistoryPanel:
    def __init__(self):
        # --- Font & UI ---
        self.font_title = pygame.font.Font("Resources/Font/pixel3.ttf", 40)
        self.font_text = pygame.font.Font("Resources/Font/pixel1.ttf", 20)
        self.ui = UIManager()

        # --- Trạng thái hiển thị ---
        self.visible = False

        # --- Ảnh nút đóng (3 trạng thái) ---
        self.close_nor = pygame.image.load("Resources/Menu/buttons/close_nor.png").convert_alpha()
        self.close_hover = pygame.image.load("Resources/Menu/buttons/close_hover.png").convert_alpha()
        self.close_pressed = pygame.image.load("Resources/Menu/buttons/close_pressed.png").convert_alpha()

        # scale nhỏ lại 0.75 để tròn hơn
        scale = 0.75
        self.close_nor = pygame.transform.smoothscale(
            self.close_nor, (int(self.close_nor.get_width()*scale), int(self.close_nor.get_height()*scale))
        )
        self.close_hover = pygame.transform.smoothscale(
            self.close_hover, (int(self.close_hover.get_width()*scale), int(self.close_hover.get_height()*scale))
        )
        self.close_pressed = pygame.transform.smoothscale(
            self.close_pressed, (int(self.close_pressed.get_width()*scale), int(self.close_pressed.get_height()*scale))
        )

        # --- Màu bảng ---
        self.panel_color = (10, 25, 60, 235)
        self.border_color = (80, 100, 160)

        # --- Preview mini mê cung ---
        try:
            self.preview_img = pygame.image.load("Resources/Menu/maze_preview.png").convert_alpha()
            self.preview_img = pygame.transform.smoothscale(self.preview_img, (130, 130))
        except:
            self.preview_img = None

        # --- Scroll ---
        self.scroll_offset = 0
        self.max_scroll = 0
        self.scroll_speed = 20

    # ------------------------------------------------------------
    def toggle(self):
        self.visible = not self.visible

    # ------------------------------------------------------------
    def handle_event(self, event):
        """Nhận sự kiện chuột cuộn"""
        if not self.visible:
            return
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset -= event.y * self.scroll_speed
            self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))

    # ------------------------------------------------------------
    def draw(self, surface, history, mouse_pos, mouse_click):
        """Vẽ Solve History overlay"""
        if not self.visible:
            return

        width, height = 850, 580
        x = RES[0] // 2 - width // 2
        y = RES[1] // 2 - height // 2

        # --- Nền panel ---
        panel_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, self.panel_color, (0, 0, width, height), border_radius=18)
        pygame.draw.rect(panel_surf, self.border_color, (0, 0, width, height), 4, border_radius=18)
        surface.blit(panel_surf, (x, y))

        # --- Tiêu đề ---
        title = self.font_title.render("Solve History", False, (255, 255, 255))
        surface.blit(title, (x + width // 2 - title.get_width() // 2, y + 20))

        # --- Nút close (hình tròn) ---
        close_img = self.close_nor
        close_rect = close_img.get_rect(center=(x + width - 45, y + 50))
        mouse_dx = mouse_pos[0] - close_rect.centerx
        mouse_dy = mouse_pos[1] - close_rect.centery
        dist = math.sqrt(mouse_dx**2 + mouse_dy**2)
        radius = close_rect.width // 2

        hovered = dist <= radius
        if hovered and mouse_click:
            close_img = self.close_pressed
            self.visible = False
            return
        elif hovered:
            close_img = self.close_hover
        else:
            close_img = self.close_nor
        surface.blit(close_img, close_rect)

        # --- Header các cột ---
        headers = ["Algorithm", "Steps", "Visited", "Generated", "Time (ms)"]
        col_x = [x + 170, x + 290, x + 400, x + 520, x + 680]
        for i, h in enumerate(headers):
            txt = self.font_text.render(h, True, (255, 220, 160))
            surface.blit(txt, (col_x[i], y + 90))
        pygame.draw.line(surface, (180, 180, 220),
                         (x + 20, y + 115), (x + width - 20, y + 115), 2)

        # --- Preview mini bản đồ ---
        if self.preview_img:
            preview_rect = self.preview_img.get_rect(topleft=(x + 25, y + 140))
            surface.blit(self.preview_img, preview_rect)

        # --- Dữ liệu lịch sử ---
        if not history:
            msg = self.font_text.render("No data yet.", True, (255, 255, 255))
            surface.blit(msg, (x + width // 2 - msg.get_width() // 2, y + height // 2))
            return

        # Dữ liệu cần vẽ
        recent = history[-30:]  # tối đa 30 dòng
        start_y = y + 130 - self.scroll_offset
        row_height = 36

        # Tính max_scroll
        total_h = len(recent) * row_height
        self.max_scroll = max(0, total_h - (height - 170))

        for i, h in enumerate(reversed(recent)):
            row_y = start_y + i * row_height
            if row_y < y + 120 or row_y > y + height - 50:
                continue  # bỏ qua dòng ngoài vùng nhìn thấy

            alg = h["algorithm"]
            steps = h.get("Độ dài đường đi: ", "-")
            visited = h.get("Số trạng thái đã duyệt: ", "-")
            gen = h.get("Số trạng thái đã sinh: ", "-")
            time_ms = round(h.get("Thời gian chạy (s): ", 0) * 1000, 1)

            vals = [alg, steps, visited, gen, time_ms]
            for j, val in enumerate(vals):
                txt = self.font_text.render(str(val), True, (255, 255, 255))
                surface.blit(txt, (col_x[j], row_y))

        # --- Thanh cuộn ---
        if self.max_scroll > 0:
            scroll_area_h = height - 180
            bar_h = max(40, int(scroll_area_h * (scroll_area_h / (total_h + 1))))
            bar_y = y + 130 + int((self.scroll_offset / self.max_scroll) * (scroll_area_h - bar_h))
            bar_rect = pygame.Rect(x + width - 18, bar_y, 8, bar_h)
            pygame.draw.rect(surface, (150, 200, 250), bar_rect, border_radius=4)
            pygame.draw.rect(surface, (60, 90, 150), (x + width - 18, y + 130, 8, scroll_area_h), 2, border_radius=4)

        # --- Viền ngoài ---
        pygame.draw.rect(surface, (100, 150, 220),
                         (x, y, width, height), 3, border_radius=18)
