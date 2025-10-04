import pygame, sys, random, math
from settings import RES
from .options import Options
from ui import UIManager   

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("Resources/Font/pixel3.ttf", 20)
        self.ui = UIManager(self.font) 

        # background
        self.bg = pygame.image.load("Resources/Menu/menu.png").convert()
        self.bg = pygame.transform.scale(self.bg, RES)

        # hiệu ứng hạt cát
        self.particles = [[random.randint(0, RES[0]), random.randint(0, RES[1]),
                           random.uniform(0.5, 2.0), random.randint(2, 4)] for _ in range(50)]
        # image buttons
        self.imgNormal = pygame.image.load("Resources/Menu/buttons/btn_bhover.png").convert_alpha()
        self.imgHover = pygame.image.load("Resources/Menu/buttons/btn_yhover.png").convert_alpha()
        self.imgPressed = pygame.image.load("Resources/Menu/buttons/btn_bpressed.png").convert_alpha()

        # toạ độ nút
        self.btn_pos = {
            "start": (RES[0]//2 - 100, 340),
            "option": (RES[0]//2 - 100, 450),
            "quit": (RES[0]//2 - 100, 560)
        }

    def draw_desert_animation(self):
        sun_center = (RES[0]-120, 100)
        for r, alpha in [(80, 30), (60, 60), (40, 120)]:
            surface = pygame.Surface(RES, pygame.SRCALPHA)
            pygame.draw.circle(surface, (255, 230, 120, alpha), sun_center, r)
            self.screen.blit(surface, (0, 0))
        pygame.draw.circle(self.screen, (255, 220, 100), sun_center, 30)

        for p in self.particles:
            x, y, speed, size = p
            pygame.draw.circle(self.screen, (230, 200, 140), (int(x), int(y)), size)
            p[0] += speed
            if p[0] > RES[0]:
                p[0] = -size
                p[1] = random.randint(0, RES[1])
                p[2] = random.uniform(0.5, 2.0)

        ticks = pygame.time.get_ticks() * 0.002
        base_y = RES[1] - 100
        for y in range(base_y, RES[1], 8):
            points = [(x, y + int(10 * math.sin(x*0.05 + ticks + y*0.1))) for x in range(0, RES[0]+20, 20)]
            pygame.draw.lines(self.screen, (220, 180, 120), False, points, 2)

    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            mouse_click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_click = True

            # vẽ nền + animation
            self.screen.blit(self.bg, (0,0))
            if self.ui.draw_image_button(self.screen, *self.btn_pos["start"],
                                        self.imgNormal, self.imgHover, self.imgPressed,
                                        mouse_pos, mouse_click, 1.5, 1.5,
                                        text="START GAME"):
                return "START GAME"

            if self.ui.draw_image_button(self.screen, *self.btn_pos["option"],
                                        self.imgNormal, self.imgHover, self.imgPressed,
                                        mouse_pos, mouse_click, 1.5, 1.5,
                                        text="OPTIONS"):
                pass

            if self.ui.draw_image_button(self.screen, *self.btn_pos["quit"],
                                        self.imgNormal, self.imgHover, self.imgPressed,
                                        mouse_pos, mouse_click, 1.5, 1.5,
                                        text="QUIT"):
                return "QUIT"

            self.draw_desert_animation()


            pygame.display.flip()
            self.clock.tick(60)
