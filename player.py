import pygame
from settings import TILE_SIZE


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, *group):
        super().__init__(*group)

        self.frame_width, self.frame_height = 96, 96
        self.sprite_idle = pygame.image.load("Resources/Characters/idle_blue.png").convert_alpha()
        self.sprite_run = pygame.image.load("Resources/Characters/run_blue.png").convert_alpha()

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

    def move_with_collision(self, dt, collision_matrix):
        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()

        # --- Trục X ---
        self.rect.x += self.direction.x * self.speed * dt
        if self.collides(self.rect, collision_matrix):
            if self.direction.x > 0:  # đi sang phải
                self.rect.right = (self.rect.right // TILE_SIZE) * TILE_SIZE
            elif self.direction.x < 0:  # đi sang trái
                self.rect.left = (self.rect.left // TILE_SIZE + 1) * TILE_SIZE

        # --- Trục Y ---
        self.rect.y += self.direction.y * self.speed * dt
        if self.collides(self.rect, collision_matrix):
            if self.direction.y > 0:  # đi xuống
                self.rect.bottom = (self.rect.bottom // TILE_SIZE) * TILE_SIZE
            elif self.direction.y < 0:  # đi lên
                self.rect.top = (self.rect.top // TILE_SIZE + 1) * TILE_SIZE


    def collides(self, rect, collision_matrix):
        rows, cols = collision_matrix.shape

        # Xác định tile mà player đang chiếm
        left = rect.left // TILE_SIZE
        right = (rect.right - 1) // TILE_SIZE
        top = rect.top // TILE_SIZE
        bottom = (rect.bottom - 1) // TILE_SIZE

        for y in range(top, bottom + 1):
            for x in range(left, right + 1):
                if 0 <= x < cols and 0 <= y < rows:
                    if collision_matrix[y][x] == 1:  # gặp tường
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
