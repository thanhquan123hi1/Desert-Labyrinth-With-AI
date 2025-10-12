import pygame
from settings import TILE_SIZE, RES
from ui import UIManager
import math


class PathViewPanel:
    def __init__(self):
        # --- Font & UI ---
        self.font_title = pygame.font.Font("Resources/Font/pixel3.ttf", 34)
        self.font_text = pygame.font.Font("Resources/Font/viethoa2.otf", 18)
        self.ui = UIManager()

        # --- Trạng thái hiển thị ---
        self.visible = False
        self.path = []
        self.map_model = None
        self.info = {}
        self.algorithm_name = "Unknown"

        # --- Nút Close (3 trạng thái) ---
        self.close_nor = pygame.image.load("Resources/Menu/buttons/close_nor.png").convert_alpha()
        self.close_hover = pygame.image.load("Resources/Menu/buttons/close_hover.png").convert_alpha()
        self.close_pressed = pygame.image.load("Resources/Menu/buttons/close_pressed.png").convert_alpha()
        scale = 0.7
        self.close_nor = pygame.transform.smoothscale(
            self.close_nor, (int(self.close_nor.get_width() * scale), int(self.close_nor.get_height() * scale))
        )
        self.close_hover = pygame.transform.smoothscale(
            self.close_hover, (int(self.close_hover.get_width() * scale), int(self.close_hover.get_height() * scale))
        )
        self.close_pressed = pygame.transform.smoothscale(
            self.close_pressed, (int(self.close_pressed.get_width() * scale), int(self.close_pressed.get_height() * scale))
        )

        # --- Màu nền ---
        self.panel_color = (10, 25, 60)
        self.border_color = (80, 100, 160)

        # --- Scroll ---
        self.scroll_offset = 0
        self.max_scroll = 0
        self.scroll_speed = 20

    # ------------------------------------------------------------
    def toggle(self, map_model=None, path=None, info=None, algorithm_name="Unknown", start=None, goal=None):
        """Bật/tắt hiển thị và cập nhật dữ liệu"""
        if map_model and path is not None:
            self.map_model = map_model
            self.path = path
            self.info = info if info else {}
            self.algorithm_name = algorithm_name
            self.start = start
            self.goal = goal
        self.visible = not self.visible


    def handle_event(self, event):
        """Nhận sự kiện cuộn chuột"""
        if not self.visible:
            return
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset -= event.y * self.scroll_speed
            self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))

    # ------------------------------------------------------------
    # ------------------------------------------------------------
    def draw(self, surface, mouse_pos, mouse_click):
        """Vẽ overlay show path"""
        if not self.visible:
            return

        width, height = 920, 560
        x = RES[0] // 2 - width // 2
        y = RES[1] // 2 - height // 2

        # --- Nền panel ---
        panel_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, self.panel_color, (0, 0, width, height), border_radius=18)
        pygame.draw.rect(panel_surf, self.border_color, (0, 0, width, height), 4, border_radius=18)
        surface.blit(panel_surf, (x, y))

        # --- Tiêu đề + tên thuật toán ---
        title = self.font_title.render("Detail", False, (255, 255, 255))
        alg_name = self.font_text.render(f"Thuật toán: {self.algorithm_name}", True, (255, 230, 180))
        surface.blit(title, (x + width // 2 - title.get_width() // 2, y + 15))
        surface.blit(alg_name, (x + 40, y + 60))

        # --- Nút close ---
        close_img = self.close_nor
        close_rect = close_img.get_rect(center=(x + width - 40, y + 45))
        dist = math.hypot(mouse_pos[0] - close_rect.centerx, mouse_pos[1] - close_rect.centery)
        hovered = dist <= close_rect.width // 2
        if hovered and mouse_click:
            close_img = self.close_pressed
            self.visible = False
            return
        elif hovered:
            close_img = self.close_hover
        surface.blit(close_img, close_rect)

        # --- Preview đường đi ---
        preview_rect = pygame.Rect(x + 35, y + 100, 480, 336)
        pygame.draw.rect(surface, (30, 40, 80), preview_rect, border_radius=10)

        if self.map_model:
            map_w = self.map_model.map_data.width * TILE_SIZE
            map_h = self.map_model.map_data.height * TILE_SIZE
            temp = pygame.Surface((map_w, map_h), pygame.SRCALPHA)

            # --- Vẽ bản đồ nền ---
            old_offx, old_offy = self.map_model.offset_x, self.map_model.offset_y
            self.map_model.offset_x = 0
            self.map_model.offset_y = 0
            self.map_model.draw(temp)
            self.map_model.offset_x, self.map_model.offset_y = old_offx, old_offy

            # --- Hiển thị đường đi ---
            if self.algorithm_name == "NoOBS":
                # Mỗi belief là một tập toạ độ => vẽ nhạt dần
                n = len(self.path)
                for i, belief in enumerate(self.path):
                    alpha = int(80 + (i / max(1, n - 1)) * 150)
                    color = (0, 255, 150, alpha)
                    for (r, c) in belief:
                        rect = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                        s.fill(color)
                        temp.blit(s, rect.topleft)

                # Vẽ viền mục tiêu
                goals = getattr(self, "goal", [])
                for (r, c) in goals:
                    pygame.draw.rect(temp, (255, 255, 0), (c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)
            else:
                # Các thuật toán thông thường
                for (r, c) in self.path:
                    rect = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                    s.fill((0, 200, 255, 100))
                    temp.blit(s, rect.topleft)

                pts = [(c * TILE_SIZE + TILE_SIZE // 2, r * TILE_SIZE + TILE_SIZE // 2) for r, c in self.path]
                if len(pts) > 1:
                    pygame.draw.lines(temp, (0, 255, 255), False, pts, 3)

            # --- Thu nhỏ ---
            scale_x = preview_rect.width / map_w
            scale_y = preview_rect.height / map_h
            scale_factor = min(scale_x, scale_y)
            new_w, new_h = int(map_w * scale_factor), int(map_h * scale_factor)
            mini = pygame.transform.smoothscale(temp, (new_w, new_h))

            offset_x = preview_rect.x + (preview_rect.width - new_w) // 2
            offset_y = preview_rect.y + (preview_rect.height - new_h) // 2
            surface.blit(mini, (offset_x, offset_y))

        # --- Thông tin tổng quát ---
        info_texts = []

        # 1️⃣ Hiển thị start / goal
        if self.algorithm_name == "NoOBS":
            starts = getattr(self, "start", [])
            goals = getattr(self, "goal", [])
            info_texts.append(("Tập trạng thái ban đầu", f"{list(starts)[:3]}{'...' if len(starts) > 3 else ''}", (120, 200, 255)))
            info_texts.append(("Tập trạng thái đích", f"{list(goals)[:3]}{'...' if len(goals) > 3 else ''}", (255, 230, 100)))
        else:
            info_texts.append(("Trạng thái bắt đầu", str(getattr(self, "start", "-")), (120, 200, 255)))
            info_texts.append(("Trạng thái đích", str(getattr(self, "goal", "-")), (255, 230, 100)))

        # 2️⃣ Các chỉ số thống kê
        info_texts.extend([
            ("Độ dài đường đi", str(self.info.get('Độ dài đường đi: ', len(self.path))), (255, 255, 255)),
            ("Số TT đã duyệt", str(self.info.get('Số trạng thái đã duyệt: ', '-')), (255, 255, 255)),
            ("Số TT đã sinh", str(self.info.get('Số trạng thái đã sinh: ', '-')), (255, 255, 255)),
            ("Thời gian chạy", f"{round(self.info.get('Thời gian chạy (s): ', 0) * 1000, 2)} ms", (255, 255, 255)),
            ("Kết quả", self.info.get('Kết quả', '—'), (0, 255, 0) if "Thành công" in self.info.get('Kết quả', '') else (255, 80, 80)),
        ])

        # 3️⃣ Vẽ text
        for i, (label, value, color) in enumerate(info_texts):
            text = f"{label}: {value}"
            txt = self.font_text.render(text, True, color)
            surface.blit(txt, (x + 550, y + 70 + i * 25))

        # --- Danh sách tọa độ ---
        if not self.path:
            msg = self.font_text.render("Không có dữ liệu đường đi.", True, (160, 195, 217))
            surface.blit(msg, (x + 600, y + 280))
            return

        # --- Hiển thị khác nhau cho NoOBS ---
        start_y = y + 270 - self.scroll_offset
        row_h = 26
        self.max_scroll = max(0, len(self.path) * row_h - 240)

        if self.algorithm_name == "NoOBS":
            for i, belief in enumerate(self.path):
                row_y = start_y + i * row_h
                if row_y < y + 270 or row_y > y + height - 70:
                    continue
                belief_preview = list(belief)[:4]
                text = f"Bước {i+1:>2}: {belief_preview}{'...' if len(belief)>4 else ''}"
                txt = self.font_text.render(text, True, (200, 255, 220))
                surface.blit(txt, (x + 550, row_y))
        else:
            for i, (r, c) in enumerate(self.path):
                row_y = start_y + i * row_h
                if row_y < y + 270 or row_y > y + height - 70:
                    continue
                text = f"{i + 1:>3}. ({r}, {c})"
                txt = self.font_text.render(text, True, (255, 255, 255))
                surface.blit(txt, (x + 550, row_y))

        # --- Thanh cuộn ---
        if self.max_scroll > 0:
            scroll_h = 240
            bar_h = max(30, int(scroll_h * (scroll_h / (len(self.path) * row_h))))
            bar_y = y + 270 + int((self.scroll_offset / self.max_scroll) * (scroll_h - bar_h))
            pygame.draw.rect(surface, (150, 200, 250), (x + width - 25, bar_y, 6, bar_h), border_radius=4)
            pygame.draw.rect(surface, (60, 90, 150), (x + width - 25, y + 270, 6, scroll_h), 2, border_radius=4)

        # --- Viền ngoài ---
        pygame.draw.rect(surface, (100, 150, 220), (x, y, width, height), 3, border_radius=18)

