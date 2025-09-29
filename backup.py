import pygame
import sys
import numpy as np
from pytmx.util_pygame import load_pygame

RES = WIDTH, HEIGHT = 1300, 750


# --- Tile class ---
class Tile(pygame.sprite.Sprite):
    def __init__(self, image, pos, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(image, (32, 32))
        self.rect = self.image.get_rect(topleft=pos)


# --- Animated Tile class ---
class AnimatedTile(pygame.sprite.Sprite):
    def __init__(self, pos, gid, map_data, *group):
        super().__init__(*group)
        self.map_data = map_data
        self.frames = []
        self.durations = []
        self.current_time = 0
        self.frame_index = 0

        # lấy animation info từ Tiled
        props = map_data.get_tile_properties_by_gid(gid)
        if props and "frames" in props:
            for frame in props["frames"]:
                img = map_data.get_tile_image_by_gid(frame.gid)
                img = pygame.transform.scale(img, (32, 32))
                self.frames.append(img)
                self.durations.append(frame.duration / 1000.0)  # ms → s

        if not self.frames:  # nếu ko có animation thì lấy frame mặc định
            img = map_data.get_tile_image_by_gid(gid)
            img = pygame.transform.scale(img, (32, 32))
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


# --- Player class ---
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, *group):
        super().__init__(*group)

        self.frame_width, self.frame_height = 96, 96
        self.sprite_idle = pygame.image.load("Resources/Characters/idle_yellow.png").convert_alpha()
        self.sprite_run = pygame.image.load("Resources/Characters/run_yellow.png").convert_alpha()

        self.num_frames_idle = 6
        self.num_frames_run = 6

        self.animations = {
            "idle": self.load_frames(self.sprite_idle, self.num_frames_idle),
            "run": self.load_frames(self.sprite_run, self.num_frames_run),
        }
        self.animation_speeds = {"idle": 0.2, "run": 0.1}

        self.state = "idle"
        self.frame_index = 0
        self.image = self.animations[self.state][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        self.speed = 200
        self.direction = pygame.math.Vector2(0, 0)
        self.facing_right = True
        self.animation_timer = 0

    def load_frames(self, sprite_sheet, num_frames):
        frames = []
        for i in range(num_frames):
            frame = sprite_sheet.subsurface(
                pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)
            )
            frame = pygame.transform.scale(frame, (64, 64))
            frames.append(frame)
        return frames

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.direction.update(0, 0)
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True

    def move(self, dt):
        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt

    def animate(self, dt):
        if self.direction.length_squared() > 0:
            self.state = "run"
        else:
            self.state = "idle"

        frames = self.animations[self.state]
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speeds[self.state]:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(frames)

        frame = frames[self.frame_index]
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)
        self.image = frame

    def update(self, dt):
        self.handle_input()
        self.move(dt)
        self.animate(dt)


# --- MapModel class ---
class MapModel:
    def __init__(self, map_file):
        self.map_data = load_pygame(map_file)
        self.sprite_group = pygame.sprite.LayeredUpdates()  # giữ đúng thứ tự layer
        self.animated_group = pygame.sprite.Group()
        self.load_layers()

    def load_layers(self):
        for layer in self.map_data.visible_layers:
            if hasattr(layer, "tiles"):
                for x, y, gid in layer:
                    if gid == 0:
                        continue
                    props = self.map_data.get_tile_properties_by_gid(gid)
                    pos = (x * self.map_data.tilewidth, y * self.map_data.tileheight)

                    if props and "frames" in props:  # tile có animation
                        AnimatedTile(pos, gid, self.map_data, self.sprite_group, self.animated_group)
                    else:  # tile thường
                        img = self.map_data.get_tile_image_by_gid(gid)
                        Tile(img, pos, self.sprite_group)

            elif hasattr(layer, "image") and layer.image:
                img = layer.image
                sprite = pygame.sprite.Sprite(self.sprite_group)
                sprite.image = img
                sprite.rect = img.get_rect(topleft=(0, 0))

    def draw(self, surface):
        self.sprite_group.draw(surface)

    def update(self, dt):
        self.animated_group.update(dt)

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


# --- Main App ---
class App:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode(RES)
        pygame.display.set_caption("MAZE")
        self.clock = pygame.time.Clock()

        self.map_model = MapModel("Resources/Maps/Map01/Map1.tmx")
        self.player_group = pygame.sprite.Group()
        self.player = Player((100, 100), self.player_group)

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

            self.player_group.update(dt)
            self.map_model.update(dt)

            self.draw()
            pygame.display.set_caption("Map Example: " + str(round(self.clock.get_fps())))
            pygame.display.flip()


if __name__ == "__main__":
    app = App()
    app.run()
