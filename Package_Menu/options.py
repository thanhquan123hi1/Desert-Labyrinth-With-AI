import pygame

class Options:
    def __init__(self, screen, font, clock):
        self.screen = screen
        self.font = font
        self.clock = clock

        # popup rect
        self.popup_rect = pygame.Rect(150, 120, 500, 350)

        # nút bấm
        self.buttons = [
            {"text": "CLOSE", "rect": pygame.Rect(320, 400, 160, 50)}
        ]

    def draw_inner_shadow(self, surface, rect, thickness=20):
        """Vẽ viền bóng đổ bên trong"""
        shadow = pygame.Surface(rect.size, pygame.SRCALPHA)
        width, height = rect.size
        for i in range(thickness):
            alpha = int(180 * (1 - i / thickness))
            pygame.draw.rect(
                shadow,
                (0, 0, 0, alpha),
                (i, i, width - 2*i, height - 2*i),
                width=3
            )
        surface.blit(shadow, rect.topleft)

    def draw_popup(self, mouse_pos):
        # overlay mờ toàn màn hình
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        # hộp popup
        pygame.draw.rect(self.screen, (240, 220, 180), self.popup_rect, border_radius=10)
        pygame.draw.rect(self.screen, (50, 30, 20), self.popup_rect, 4, border_radius=10)
        self.draw_inner_shadow(self.screen, self.popup_rect)

        # tiêu đề
        title = self.font.render("OPTIONS", True, (0, 0, 0))
        self.screen.blit(title, (self.popup_rect.centerx - title.get_width()//2, self.popup_rect.y + 20))

        # vẽ các nút
        for btn in self.buttons:
            rect = btn["rect"]
            color = (200, 170, 120) if rect.collidepoint(mouse_pos) else (180, 140, 100)
            pygame.draw.rect(self.screen, color, rect, border_radius=5)
            pygame.draw.rect(self.screen, (0,0,0), rect, 3, border_radius=5)

            text = self.font.render(btn["text"], True, (255,255,255))
            self.screen.blit(text, (rect.centerx - text.get_width()//2,
                                    rect.centery - text.get_height()//2))

    def show(self):
        """Chạy popup cho đến khi bấm CLOSE"""
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_click = True

            # Vẽ popup (đè lên menu đang hiển thị phía dưới)
            self.draw_popup(mouse_pos)

            # xử lý nút
            for btn in self.buttons:
                if mouse_click and btn["rect"].collidepoint(mouse_pos):
                    if btn["text"] == "CLOSE":
                        running = False

            pygame.display.flip()
            self.clock.tick(60)
