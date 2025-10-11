import pygame
from settings import RES

class Fade:
    def __init__(self, color=(0, 0, 0)):
        self.color = color
        self.alpha = 0
        self.speed = 8
        self.active = False
        self.mode = None      # "in" hoặc "out"
        self.surface = pygame.Surface(RES)
        self.surface.fill(color)
        self.surface.set_alpha(0)
        self.cycle = False    # có tự động chuyển ngược lại sau khi xong không

    def start(self, mode="out", auto_reverse=False):
        """
        mode = 'out' → fade tối dần
        mode = 'in'  → fade sáng dần
        auto_reverse = True → tự động thực hiện fade ngược lại sau khi xong
        """
        self.mode = mode
        self.active = True
        self.cycle = auto_reverse
        self.alpha = 0 if mode == "out" else 255
        self.surface.set_alpha(self.alpha)

    def update(self, screen):
        """Cập nhật hiệu ứng fade, trả về True khi đã hoàn tất toàn bộ (kể cả chu kỳ nếu có)."""
        if not self.active:
            return True

        done_one_cycle = False

        # --- xử lý fade ra / vào ---
        if self.mode == "out":
            self.alpha += self.speed
            if self.alpha >= 255:
                self.alpha = 255
                done_one_cycle = True
        else:  # fade in
            self.alpha -= self.speed
            if self.alpha <= 0:
                self.alpha = 0
                done_one_cycle = True

        # --- nếu hoàn tất một pha và có auto_reverse ---
        if done_one_cycle:
            if self.cycle:
                self.cycle = False  # chỉ thực hiện 1 lần chu kỳ
                self.mode = "in" if self.mode == "out" else "out"
            else:
                self.active = False

        # --- vẽ fade lên màn hình ---
        self.surface.set_alpha(self.alpha)
        screen.blit(self.surface, (0, 0))

        return not self.active  # True nếu toàn bộ fade (cả 2 pha) đã kết thúc
