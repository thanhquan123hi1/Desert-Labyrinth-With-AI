import pygame, sys
from settings import RES
from map_model import MapModel
from player import Player
from ui import UIManager
from menu import Menu


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

    def draw(self):
        self.surface.blit(self.bg, (0, 0))
        self.map_model.draw(self.surface)
        self.ui.draw_panel(self.surface, 1020,30,400,680, "CONTROL PANEL")
        self.player_group.draw(self.surface)

    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.player_group.update(dt, self.map_model.collision_matrix)
            self.map_model.update(dt)

            self.draw()
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
        ui.fade_transition(screen, clock, RES, 1500)  # hiệu ứng 1.5s
        app = App()
        app.run()

