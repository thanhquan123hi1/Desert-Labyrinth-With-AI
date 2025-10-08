import pygame, sys
from settings import RES
from .options import Options
from ui import UIManager
from Package_Animation import Particles

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

        # toạ độ nút
        self.btn_pos = {
            "start": (RES[0] // 2 - 100, 340),
            "option": (RES[0] // 2 - 100, 450),
            "quit": (RES[0] // 2 - 100, 560)
        }

        # hiệu ứng sa mạc (hạt cát bay, mặt trời, sóng cát)
        self.effect = Particles()

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
            self.screen.blit(self.bg, (0, 0))

            # vẽ buttons
            if self.ui.draw_image_button(self.screen, *self.btn_pos["start"],
                                         self.imgNormal, self.imgHover, self.imgPressed,
                                         mouse_pos, mouse_click, 1.5, 1.5,
                                         text="START GAME"):
                return "START GAME"

            if self.ui.draw_image_button(self.screen, *self.btn_pos["option"],
                                         self.imgNormal, self.imgHover, self.imgPressed,
                                         mouse_pos, mouse_click, 1.5, 1.5,
                                         text="OPTIONS"):
                return "OPTIONS"

            if self.ui.draw_image_button(self.screen, *self.btn_pos["quit"],
                                         self.imgNormal, self.imgHover, self.imgPressed,
                                         mouse_pos, mouse_click, 1.5, 1.5,
                                         text="QUIT"):
                return "QUIT"

            # vẽ hiệu ứng sa mạc
            self.effect.sandstormEffect(self.screen)

            # cập nhật màn hình
            pygame.display.flip()
            self.clock.tick(60)
