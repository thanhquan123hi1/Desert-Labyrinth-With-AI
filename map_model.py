import pygame
import numpy as np
from pytmx.util_pygame import load_pygame

from tile import Tile, AnimatedTile


class MapModel:
    def __init__(self, map_file, offset=(0, 0)):
        self.map_data = load_pygame(map_file)
        self.offset_x, self.offset_y = offset
        self.sprite_group = pygame.sprite.LayeredUpdates()
        self.animated_group = pygame.sprite.Group()
        self.load_layers()
        self.collision_matrix = self.get_collision_matrix()

    # ----------------------------------------------------------------
    def load_layers(self):
        for layer in self.map_data.visible_layers:
            if hasattr(layer, "tiles"):
                for x, y, gid in layer:
                    if gid == 0:
                        continue
                    props = self.map_data.get_tile_properties_by_gid(gid)
                    pos = (
                        x * self.map_data.tilewidth + self.offset_x,
                        y * self.map_data.tileheight + self.offset_y
                    )

                    if props and "frames" in props:
                        AnimatedTile(pos, gid, self.map_data, self.sprite_group, self.animated_group)
                    else:
                        img = self.map_data.get_tile_image_by_gid(gid)
                        Tile(img, pos, self.sprite_group)

            elif hasattr(layer, "image") and layer.image:
                img = layer.image
                sprite = pygame.sprite.Sprite(self.sprite_group)
                sprite.image = img
                sprite.rect = img.get_rect(topleft=(self.offset_x, self.offset_y))

    # ----------------------------------------------------------------
    def draw(self, surface):
        self.sprite_group.draw(surface)

    def update(self, dt):
        self.animated_group.update(dt)

    # ----------------------------------------------------------------
    def get_collision_matrix(self, layer_name="collision"):
        """Tạo ma trận 0/1 (ô trống / ô tường)"""
        width, height = self.map_data.width, self.map_data.height
        matrix = np.zeros((height, width), dtype=int)

        for layer in self.map_data.layers:
            if layer.name == layer_name and hasattr(layer, "data"):
                for y in range(height):
                    for x in range(width):
                        tile = layer.data[y][x]
                        if tile:
                            matrix[y][x] = 1
                break
        return matrix


