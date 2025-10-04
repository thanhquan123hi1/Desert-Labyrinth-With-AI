import pygame
from settings import TILE_SIZE


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
            frame = pygame.transform.scale(frame, (40, 40))
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

    def move_with_collision(self, dt, collision_matrix):
        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()

        new_x = self.rect.x + self.direction.x * self.speed * dt
        new_y = self.rect.y + self.direction.y * self.speed * dt

        # --- Trục X ---
        future_rect = self.rect.copy()
        future_rect.x = new_x
        if not self.collides(future_rect, collision_matrix):
            self.rect.x = new_x

        # --- Trục Y ---
        future_rect = self.rect.copy()
        future_rect.y = new_y
        if not self.collides(future_rect, collision_matrix):
            self.rect.y = new_y

    def collides(self, rect, collision_matrix):
        rows, cols = collision_matrix.shape
        top_left = (rect.left // TILE_SIZE, rect.top // TILE_SIZE)
        bottom_right = (rect.right // TILE_SIZE, rect.bottom // TILE_SIZE)

        for y in range(top_left[1], bottom_right[1] + 1):
            for x in range(top_left[0], bottom_right[0] + 1):
                if 0 <= x < cols and 0 <= y < rows:
                    if collision_matrix[y][x] == 1:
                        return True
        return False

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

    def update(self, dt, collision_matrix):
        self.handle_input()
        self.move_with_collision(dt, collision_matrix)
        self.animate(dt)
