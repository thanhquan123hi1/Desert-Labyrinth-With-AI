import pygame
import numpy as np
from tile import Tile, AnimatedTile
from pytmx.util_pygame import load_pygame #đối tượng để load file tmx
from BFS import BFS


class MapModel:
    def __init__(self, map_file):
        self.map_data = load_pygame(map_file)
        self.sprite_group = pygame.sprite.LayeredUpdates() #tạo một nhóm sprite theo layer trong file tmx
        self.animated_group = pygame.sprite.Group()   #nhóm các sprite động lại
        self.load_layers()  #phương thức load_layers
        self.collision_matrix = self.get_collision_matrix() #lấy mà trận để trả về các class Thuật toán và Player

    def load_layers(self):
        for layer in self.map_data.visible_layers:
            if hasattr(layer, "tiles"): #kiểm tra xem layer đó có thuộc tính nào là tiles ko
                for x, y, gid in layer:
                    if gid == 0:
                        continue
                    props = self.map_data.get_tile_properties_by_gid(gid) #thông tin cấu hình bổ sung của từng tile(có thể đi qua hay va chạm)
                    pos = (x * self.map_data.tilewidth, y * self.map_data.tileheight)

                    if props and "frames" in props: #Xử lý với tile động(tile có nhãn frames và có thông tin bổ sung
                        AnimatedTile(pos, gid, self.map_data, self.sprite_group, self.animated_group)
                    else: #Xử lý với tile tĩnh(tile có thông tin bổ sung)
                        img = self.map_data.get_tile_image_by_gid(gid)
                        Tile(img, pos, self.sprite_group)

            elif hasattr(layer, "image") and layer.image:
                img = layer.image
                sprite = pygame.sprite.Sprite(self.sprite_group)
                sprite.image = img
                sprite.rect = img.get_rect(topleft=(0, 0))

    def draw(self, surface):
        self.sprite_group.draw(surface) #Vẽ các sprite trong nhóm sprite_group nhờ vào hàm có sẳn draw

    def update(self, dt):
        self.animated_group.update(dt)  #Cập nhật các sprite trong nhóm animated_group nhờ vào hàm có sẳn update

    def get_collision_matrix(self, layer_name="collision"):
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



