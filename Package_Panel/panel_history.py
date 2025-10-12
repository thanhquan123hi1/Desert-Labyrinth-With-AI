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

        # --- Ảnh nút đóng ---
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

        # --- Scroll ---
        self.scroll_offset = 0
        self.max_scroll = 0
        self.scroll_speed = 20

    # ------------------------------------------------------------
    def toggle(self):
        self.visible = not self.visible

    # ------------------------------------------------------------
    def handle_event(self, event):
        if not self.visible:
            return
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset -= event.y * self.scroll_speed
            self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))

    # ------------------------------------------------------------
    def draw(self, surface, history, mouse_pos, mouse_click):
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

        # --- Nút close ---
        close_img = self.close_nor
        close_rect = close_img.get_rect(center=(x + width - 45, y + 50))
        hovered = math.hypot(mouse_pos[0] - close_rect.centerx, mouse_pos[1] - close_rect.centery) <= close_rect.width // 2
        if hovered and mouse_click:
            close_img = self.close_pressed
            self.visible = False
            return
        elif hovered:
            close_img = self.close_hover
        surface.blit(close_img, close_rect)

        # --- Header các cột ---
        headers = ["Algorithm", "Steps", "Visited", "Generated", "Time (ms)", "Result"]
        col_x = [x + 100, x + 220, x + 330, x + 460, x + 590, x + 720]
        for i, h in enumerate(headers):
            txt = self.font_text.render(h, False, (255, 220, 160))
            surface.blit(txt, (col_x[i], y + 90))
        pygame.draw.line(surface, (180, 180, 220), (x + 20, y + 115), (x + width - 20, y + 115), 2)

        # --- Không có dữ liệu ---
        if not history:
            msg = self.font_text.render("No data yet.", False, (255, 255, 255))
            surface.blit(msg, (x + width // 2 - msg.get_width() // 2, y + height // 2))
            return

        # --- Dữ liệu lịch sử ---
        recent = history[-30:]  # tối đa 30 dòng
        start_y = y + 130 - self.scroll_offset
        row_height = 36
        total_h = len(recent) * row_height
        self.max_scroll = max(0, total_h - (height - 170))

        for i, h in enumerate(reversed(recent)):
            row_y = start_y + i * row_height
            if row_y < y + 120 or row_y > y + height - 50:
                continue

            alg = h["algorithm"]
            steps = h.get("Độ dài đường đi: ", "-")
            visited = h.get("Số trạng thái đã duyệt: ", "-")
            gen = h.get("Số trạng thái đã sinh: ", "-")
            time_ms = round(h.get("Thời gian chạy (s): ", 0) * 1000, 1)
            result = h.get("Kết quả", "—")

            vals = [alg, steps, visited, gen, time_ms]
            for j, val in enumerate(vals):
                txt = self.font_text.render(str(val), True, (255, 255, 255))
                surface.blit(txt, (col_x[j], row_y))

            # 🔹 Cột “Kết quả” màu sắc
            if result == "Thành công": result = "success" 
            else: result = "fail"
            color = (0, 255, 0) if result == "success" else (255, 80, 80)
            res_txt = self.font_text.render(result, False, color)
            surface.blit(res_txt, (col_x[-1], row_y))

        # --- Thanh cuộn ---
        if self.max_scroll > 0:
            scroll_area_h = height - 180
            bar_h = max(40, int(scroll_area_h * (scroll_area_h / (total_h + 1))))
            bar_y = y + 130 + int((self.scroll_offset / self.max_scroll) * (scroll_area_h - bar_h))
            pygame.draw.rect(surface, (150, 200, 250), (x + width - 18, bar_y, 8, bar_h), border_radius=4)
            pygame.draw.rect(surface, (60, 90, 150), (x + width - 18, y + 130, 8, scroll_area_h), 2, border_radius=4)

        # --- Viền ngoài ---
        pygame.draw.rect(surface, (100, 150, 220), (x, y, width, height), 3, border_radius=18)
