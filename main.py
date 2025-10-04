import pygame, sys
from settings import RES
from map_model import MapModel
from player import Player
from ui import UIManager
from Package_Menu import Menu, Options


class App:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode(RES)
        self.bg = pygame.image.load("Resources/Maps/desert.png")
        pygame.display.set_caption("MAZE")
        self.clock = pygame.time.Clock()
        
        self.map_model = MapModel("Resources/Maps/Map1.tmx")
        self.ui = UIManager()
        self.player_group = pygame.sprite.Group()
        self.player = Player((96, 96), self.player_group)  

        # image buttons
        self.imgNormal = pygame.image.load("Resources/Menu/buttons/Button_Blue.png").convert_alpha()
        self.imgHover = pygame.image.load("Resources/Menu/buttons/Button_Hover.png").convert_alpha()
        self.imgPressed = pygame.image.load("Resources/Menu/buttons/Button_Blue_Pressed.png").convert_alpha()
        # nút back
        self.imgNormal_back = pygame.image.load("Resources/Maps/buttons/back_normal.png").convert_alpha()
        self.imgHover_back = pygame.image.load("Resources/Maps/buttons/back_hover.png").convert_alpha()
        self.imgPressed_back = pygame.image.load("Resources/Maps/buttons/back_pressed.png").convert_alpha()

    def draw(self):
        self.surface.blit(self.bg, (0, 0))
        self.map_model.draw(self.surface)
        self.ui.draw_panel(self.surface, 1020,30,420,700, "Information panel")
        self.player_group.draw(self.surface)

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

            dt = self.clock.tick(60) / 1000


            self.player_group.update(dt, self.map_model.collision_matrix)
            self.map_model.update(dt)

            self.draw()

            self.ui.draw_image_button(self.surface, 1322, 615, 
                                      self.imgNormal, self.imgHover, self.imgPressed ,mouse_pos, mouse_click, 1.2, 1.2)
            
            self.ui.draw_image_button(self.surface, 0, 0, 
                                      self.imgNormal_back, self.imgHover_back, self.imgPressed_back ,mouse_pos, mouse_click, 1, 1)
            
            pygame.display.set_caption("Map: " + str(round(self.clock.get_fps())))
            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(RES)
    clock = pygame.time.Clock()

    # chạy menu
    menu = Menu(screen)
    choice = menu.run()

    if choice == "START GAME":
        ui = UIManager()
        ui.fade_transition(screen, clock, RES, 1000)
        app = App()
        app.run()

