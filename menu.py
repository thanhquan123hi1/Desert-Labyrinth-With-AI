import pygame, sys, random
from settings import RES
import math


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

        # load background
        self.bg = pygame.image.load("Resources/Menu/menu.png").convert()
        self.bg = pygame.transform.scale(self.bg, RES)

        # font
        self.btn_font = pygame.font.Font("Resources/Font/pixel2.ttf", 40)
        self.small_font = pygame.font.Font("Resources/Font/pixel2.ttf", 28)

        # button list
        self.buttons = [
            {"text": "START GAME", "rect": pygame.Rect(RES[0]//2 - 150, 350, 320, 70)},
            {"text": "OPTIONS", "rect": pygame.Rect(RES[0]//2 - 150, 450, 320, 70)},
            {"text": "EXIT", "rect": pygame.Rect(RES[0]//2 - 150, 550, 320, 70)},
        ]

        # desert particles (bụi/cát bay)
        self.particles = []
        for _ in range(50):
            x = random.randint(0, RES[0])
            y = random.randint(0, RES[1])
            speed = random.uniform(0.5, 2.0)
            size = random.randint(2, 4)
            self.particles.append([x, y, speed, size])

    def draw_button(self, btn, mouse_pos):
        rect = btn["rect"]
        color = (200, 170, 120) if rect.collidepoint(mouse_pos) else (180, 140, 100)
        pygame.draw.rect(self.screen, color, rect, border_radius=5)
        pygame.draw.rect(self.screen, (0,0,0), rect, 3, border_radius=5)

        text = self.btn_font.render(btn["text"], False, (255,255,255))
        self.screen.blit(text, (rect.centerx - text.get_width()//2,
                                rect.centery - text.get_height()//2))

    # ================= DESERT ANIMATION =================
    def draw_desert_animation(self):
        # mặt trời + halo
        sun_center = (RES[0]-120, 100)
        for r, alpha in [(80, 30), (60, 60), (40, 120)]:  # vẽ halo mờ dần
            surface = pygame.Surface(RES, pygame.SRCALPHA)
            pygame.draw.circle(surface, (255, 230, 120, alpha), sun_center, r)
            self.screen.blit(surface, (0, 0))
        pygame.draw.circle(self.screen, (255, 220, 100), sun_center, 30)

        # bụi/cát bay
        for p in self.particles:
            x, y, speed, size = p
            pygame.draw.circle(self.screen, (230, 200, 140), (int(x), int(y)), size)
            p[0] += speed
            if p[0] > RES[0]:
                p[0] = -size
                p[1] = random.randint(0, RES[1])
                p[2] = random.uniform(0.5, 2.0)

        # cát gợn sóng
        ticks = pygame.time.get_ticks() * 0.002
        base_y = RES[1] - 100
        for y in range(base_y, RES[1], 8):  # nhiều lớp sóng nhỏ
            points = []
            for x in range(0, RES[0]+20, 20):
                offset = int(10 * math.sin(x*0.05 + ticks + y*0.1))
                points.append((x, y + offset))
            if len(points) > 1:
                pygame.draw.lines(self.screen, (220, 180, 120), False, points, 2)


    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_click = True

            # vẽ background
            self.screen.blit(self.bg, (0,0))

            # vẽ desert animation
            self.draw_desert_animation()

            # vẽ buttons
            for btn in self.buttons:
                self.draw_button(btn, mouse_pos)
                if mouse_click and btn["rect"].collidepoint(mouse_pos):
                    if btn["text"] == "EXIT":
                        pygame.quit()
                        sys.exit()
                    return btn["text"]   # >>> trả về lựa chọn

            # vẽ dòng nhỏ dưới cùng
            press_text = self.small_font.render("PRESS START", False, (255,255,255))
            self.screen.blit(press_text, (RES[0]//2 - press_text.get_width()//2, 650))

            pygame.display.flip()
            self.clock.tick(60)

# ----------------- MAIN DEMO -----------------
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(RES)
    pygame.display.set_caption("Main Menu")

    menu = Menu(screen)
    menu.run()
