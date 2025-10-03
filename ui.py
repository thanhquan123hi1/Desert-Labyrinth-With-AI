import pygame

class UIManager:
    def __init__(self, font=None):
        if font is None:
            self.font = pygame.font.SysFont("Arial", 20)
        else:
            self.font = font

    def fade_transition(self, screen, clock, res, duration=1000):
        """Hiệu ứng fade (đen -> sáng) khi chuyển cảnh"""
        fade_surface = pygame.Surface(res)
        fade_surface.fill((0, 0, 0))

        start_time = pygame.time.get_ticks()
        running = True
        while running:
            now = pygame.time.get_ticks()
            elapsed = now - start_time
            if elapsed > duration:
                running = False
                elapsed = duration

            # alpha từ 0 -> 255 -> 0
            if elapsed <= duration // 2:
                alpha = int(255 * (elapsed / (duration // 2)))
            else:
                alpha = int(255 * (1 - (elapsed - duration // 2) / (duration // 2)))

            fade_surface.set_alpha(alpha)
            screen.blit(fade_surface, (0, 0))

            pygame.display.flip()
            clock.tick(60)

    # ================= PANEL =================
    def draw_panel(self, surface, x, y, width, height, title=None):
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, (230, 230, 230), rect)  # nền
        pygame.draw.rect(surface, (0, 0, 0), rect, 2)    # viền
        if title:
            text = self.font.render(title, False, (0, 0, 0))
            surface.blit(text, (x + 10, y + 10))
        return rect

    # ================= BUTTON =================
    def draw_button(self, surface, x, y, width, height, text, mouse_pos, mouse_click):
        rect = pygame.Rect(x, y, width, height)
        color = (200, 200, 200)
        if rect.collidepoint(mouse_pos):
            color = (180, 180, 180)
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, (0, 0, 0), rect, 2)
        text_surf = self.font.render(text, False, (0,0,0))
        surface.blit(text_surf, (rect.centerx - text_surf.get_width()//2,
                                 rect.centery - text_surf.get_height()//2))
        if mouse_click and rect.collidepoint(mouse_pos):
            return True
        return False

    # ================= DROPMENU =================
    def draw_dropmenu(self, surface, x, y, width, height, options, state, mouse_pos, mouse_click):
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, (240, 240, 240), rect)
        pygame.draw.rect(surface, (0, 0, 0), rect, 2)

        if state["selected"]:
            txt = self.font.render(state["selected"], False, (0,0,0))
            surface.blit(txt, (x+5, y+5))

        if mouse_click and rect.collidepoint(mouse_pos):
            state["open"] = not state["open"]

        chosen = None
        if state["open"]:
            for i, opt in enumerate(options):
                r = pygame.Rect(x, y + (i+1)*height, width, height)
                pygame.draw.rect(surface, (255,255,255), r)
                pygame.draw.rect(surface, (0,0,0), r, 1)
                txt = self.font.render(opt, False, (0,0,0))
                surface.blit(txt, (r.x+5, r.y+5))

                if mouse_click and r.collidepoint(mouse_pos):
                    state["selected"] = opt
                    state["open"] = False
                    chosen = opt
        return chosen

    # ================= IMAGE BUTTON =================
    def draw_image_button(self, surface, x, y, images, mouse_pos, mouse_pressed):
        if not hasattr(self, "_cache"):
            self._cache = {}
        if images["normal"] not in self._cache:
            self._cache[images["normal"]]  = pygame.image.load(images["normal"]).convert_alpha()
            self._cache[images["hover"]]   = pygame.image.load(images["hover"]).convert_alpha()
            self._cache[images["pressed"]] = pygame.image.load(images["pressed"]).convert_alpha()

        img_normal  = self._cache[images["normal"]]
        img_hover   = self._cache[images["hover"]]
        img_pressed = self._cache[images["pressed"]]

        rect = img_normal.get_rect(center=(x, y))

        clicked = False
        if rect.collidepoint(mouse_pos):
            if mouse_pressed[0]:
                surface.blit(img_pressed, rect)
                self._was_pressed = True
            else:
                surface.blit(img_hover, rect)
                if getattr(self, "_was_pressed", False):
                    clicked = True
                self._was_pressed = False
        else:
            surface.blit(img_normal, rect)

        return clicked


# ================= DEMO =================
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Demo UI Manager")

    ui = UIManager(pygame.font.SysFont("Arial", 20))
    drop_state = {"open": False, "selected": "BFS"}
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        mouse_pressed = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = True

        screen.fill((255, 255, 255))

        # Panel
        ui.draw_panel(screen, 50, 50, 500, 400, "Control Panel")

        # Normal button
        if ui.draw_button(screen, 70, 100, 120, 40, "Run", mouse_pos, mouse_click):
            print("Run clicked")

        # Dropmenu
        selected = ui.draw_dropmenu(screen, 70, 160, 150, 30,
                                    ["BFS", "DFS", "A*"], drop_state,
                                    mouse_pos, mouse_click)
        if selected:
            print("Selected:", selected)

        # Image button demo (bỏ width, height để không bị lỗi)
        if ui.draw_image_button(screen, 300, 500,
                                {"normal":"Resources/Menu/play_nor.png",
                                 "hover":"Resources/Menu/play_Hover.png",
                                 "pressed":"Resources/Menu/play_Pressed.png"},
                                mouse_pos, mouse_pressed):
            print("Play button clicked")

        pygame.display.flip()
    pygame.quit()
