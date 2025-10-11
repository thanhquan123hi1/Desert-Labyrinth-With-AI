import pygame
import matplotlib.pyplot as plt
from io import BytesIO
from settings import RES
from ui import UIManager
import math


class ChartPanel:
    def __init__(self):
        # --- Font & UI ---
        self.ui = UIManager()
        self.font_title = pygame.font.Font("Resources/Font/pixel3.ttf", 36)
        self.font_text = pygame.font.Font("Resources/Font/viethoa2.otf", 22)

        # --- Trạng thái hiển thị ---
        self.visible = False
        self.history = []
        self.alpha = 0
        self.fade_in_speed = 12

        # --- Nút close ---
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

        # --- Màu nền panel ---
        self.panel_color = (10, 25, 60)
        self.border_color = (80, 100, 160)

        # --- Lưu chart image ---
        self.chart_img = None

    # ------------------------------------------------------------
    def toggle(self, history):
        """Bật/tắt hiển thị và cập nhật dữ liệu"""
        self.visible = not self.visible
        self.history = history
        self.alpha = 0
        if self.visible:
            self.chart_img = self.make_chart()

    # ------------------------------------------------------------
    def make_chart(self):
        """Tạo biểu đồ matplotlib từ dữ liệu"""
        if not self.history:
            return None

        # gom kết quả cuối cùng của mỗi thuật toán
        data = {}
        for h in self.history:
            data[h["algorithm"]] = h

        algs = list(data.keys())
        times = [data[a]["Thời gian chạy (s): "] for a in algs]
        states = [data[a]["Số trạng thái đã sinh: "] for a in algs]

        # --- tạo biểu đồ kép ---
        fig, ax1 = plt.subplots(figsize=(6, 4), dpi=120)
        ax1.bar(algs, times, color="#f4b942", label="Thời gian (s)", alpha=0.8)
        ax1.set_ylabel("Thời gian (s)", color="#f4b942", fontsize=10)
        ax1.tick_params(axis='y', labelcolor="#f4b942")

        ax2 = ax1.twinx()
        ax2.plot(algs, states, 'o-', color="#42a5f5", label="TT sinh ra")
        ax2.set_ylabel("Số trạng thái sinh ra", color="#42a5f5", fontsize=10)
        ax2.tick_params(axis='y', labelcolor="#42a5f5")
        
        ax1.set_xlabel("Thuật toán", color="white", fontsize=10)
        ax1.tick_params(axis='x', colors="white")

        fig.suptitle("So sánh hiệu năng giữa các thuật toán", fontsize=15, color="white")
        fig.patch.set_facecolor("#1c1f3a")
        ax1.set_facecolor("#1c1f3a")

        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', facecolor=fig.get_facecolor())
        buf.seek(0)
        plt.close(fig)

        chart = pygame.image.load(buf, 'png').convert()
        chart = pygame.transform.smoothscale(chart, (760, 460))
        return chart

    # ------------------------------------------------------------
    def draw(self, surface, mouse_pos, mouse_click):
        """Vẽ chart panel (gọi trong vòng lặp game chính)"""
        if not self.visible:
            return

        width, height = 860, 580
        x = RES[0] // 2 - width // 2
        y = RES[1] // 2 - height // 2

        # --- Fade in ---
        if self.alpha < 230:
            self.alpha = min(230, self.alpha + self.fade_in_speed)

        # --- Panel nền ---
        panel_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, (*self.panel_color, self.alpha), (0, 0, width, height), border_radius=18)
        pygame.draw.rect(panel_surf, self.border_color, (0, 0, width, height), 4, border_radius=18)

        surface.blit(panel_surf, (x, y))


        # --- Tiêu đề ---
        title = self.font_title.render("Chart", False, (255, 255, 255))
        surface.blit(title, (x + width // 2 - title.get_width() // 2, y + 20))

        # --- Nút Close ---
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

        # --- Chart ---
        if self.chart_img:
            surface.blit(self.chart_img, (x + 50, y + 90))
        else:
            msg = self.font_text.render("Chưa có dữ liệu để vẽ biểu đồ!", False, (255, 255, 255))
            surface.blit(msg, (x + width // 2 - msg.get_width() // 2, y + height // 2 - 20))

        # --- Viền ngoài ---
        pygame.draw.rect(surface, (100, 150, 220), (x, y, width, height), 3, border_radius=18)
