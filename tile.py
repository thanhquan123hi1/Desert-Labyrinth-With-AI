import pygame

from settings import TILE_SIZE


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, pos, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)


class AnimatedTile(pygame.sprite.Sprite):
    def __init__(self, pos, gid, map_data, *group):
        super().__init__(*group)
        self.map_data = map_data
        self.frames, self.durations = [], []
        self.current_time, self.frame_index = 0, 0

        props = map_data.get_tile_properties_by_gid(gid)
        if props and "frames" in props:
            for frame in props["frames"]:
                img = map_data.get_tile_image_by_gid(frame.gid)
                img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                self.frames.append(img)
                self.durations.append(frame.duration / 1000.0)  # ms → s

        if not self.frames:  
            img = map_data.get_tile_image_by_gid(gid)
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            self.frames.append(img)
            self.durations.append(1.0)

        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, dt):
        if len(self.frames) > 1:
            self.current_time += dt
            if self.current_time >= self.durations[self.frame_index]:
                self.current_time = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.image = self.frames[self.frame_index]
