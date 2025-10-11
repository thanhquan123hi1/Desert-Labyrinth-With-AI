import pygame, sys
from settings import RES
from .options import Options
from ui import UIManager
from Package_Animation import Particles, Fade


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("Resources/Font/pixel3.ttf", 20)
        self.ui = UIManager(self.font)

        # background
        self.bg = pygame.image.load("Resources/Menu/menu.png").convert()
        self.bg = pygame.transform.scale(self.bg, RES)

        # image buttons
        self.imgNormal = pygame.image.load("Resources/Menu/buttons/btn_bhover.png").convert_alpha()
        self.imgHover = pygame.image.load("Resources/Menu/buttons/btn_yhover.png").convert_alpha()
        self.imgPressed = pygame.image.load("Resources/Menu/buttons/btn_bpressed.png").convert_alpha()

        # vị trí nút
        self.btn_pos = {
            "start": (RES[0] // 2 - 100, 340),
            "option": (RES[0] // 2 - 100, 450),
            "quit": (RES[0] // 2 - 100, 560)
        }

        # hiệu ứng nền
        self.effect = Particles()

        # hiệu ứng chuyển cảnh
        self.fade = Fade((0, 0, 0))
        self.fade.start("in")   # fade in khi mở menu

    # --------------------------------------------------------
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

            # vẽ nền
            self.screen.blit(self.bg, (0, 0))

            # hiệu ứng cát bay
            self.effect.desertEffect(self.screen)

            # --- BUTTONS ---
            if self.ui.draw_image_button(self.screen, *self.btn_pos["start"],
                                         self.imgNormal, self.imgHover, self.imgPressed,
                                         mouse_pos, mouse_click, 1.5, 1.5, text="START GAME"):
                self.fade.start("out")
                while self.fade.active:
                    self.screen.blit(self.bg, (0, 0))
                    self.effect.desertEffect(self.screen)
                    self.fade.update(self.screen)
                    pygame.display.flip()
                return "START GAME"

            if self.ui.draw_image_button(self.screen, *self.btn_pos["option"],
                                         self.imgNormal, self.imgHover, self.imgPressed,
                                         mouse_pos, mouse_click, 1.5, 1.5, text="OPTIONS"):
                self.fade.start("out")
                while self.fade.active:
                    self.screen.blit(self.bg, (0, 0))
                    self.effect.desertEffect(self.screen)
                    self.fade.update(self.screen)
                    pygame.display.flip()
                return "OPTIONS"

            if self.ui.draw_image_button(self.screen, *self.btn_pos["quit"],
                                         self.imgNormal, self.imgHover, self.imgPressed,
                                         mouse_pos, mouse_click, 1.5, 1.5, text="QUIT"):
                return "QUIT"

            if self.fade.active:
                self.fade.update(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
