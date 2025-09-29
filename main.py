import pygame, sys
from settings import RES
from map_model import MapModel
from player import Player


class App:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode(RES)
        pygame.display.set_caption("MAZE")
        self.clock = pygame.time.Clock()

        self.map_model = MapModel("Resources/Maps/Map1.tmx")
        self.player_group = pygame.sprite.Group()
        self.player = Player((40, 40), self.player_group)

    def draw(self):
        self.surface.fill("black")
        self.map_model.draw(self.surface)
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
    app = App()
    app.run()
