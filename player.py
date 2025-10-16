import pygame
from settings import TILE_SIZE
from Package_Animation import SpriteSheetAnimation
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, *group, 
                 sprite_idle=("Resources/Characters/idle_torchman.png", 96, 96, 6),
                 sprite_run=None,
                 offset=(0, 0)):
        super().__init__(*group)

        self.offset_x, self.offset_y = offset

        # --- Idle sheet ---
        idle_path, self.frame_width, self.frame_height, self.num_frames_idle = sprite_idle
        self.sprite_idle = pygame.image.load(idle_path).convert_alpha()

        # --- Run sheet ---
        if sprite_run:
            run_path, _, _, self.num_frames_run = sprite_run
            self.sprite_run = pygame.image.load(run_path).convert_alpha()
        else:
            self.sprite_run = self.sprite_idle
            self.num_frames_run = self.num_frames_idle

        # --- Animations ---
        self.animations = {
            "idle": self.load_frames(self.sprite_idle, self.num_frames_idle),
            "run":  self.load_frames(self.sprite_run, self.num_frames_run),
        }
        self.animation_speeds = {"idle": 0.1, "run": 0.1}

        # --- Trạng thái mặc định ---
        self.state = "idle"
        self.frame_index = 0
        self.image = self.animations[self.state][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        # --- Di chuyển ---
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

        # --- Tạm thời loại bỏ offset khi kiểm tra va chạm ---
        rect = self.rect.copy()
        rect.x -= self.offset_x
        rect.y -= self.offset_y

        # Trục X
        rect.x += self.direction.x * self.speed * dt
        if self.collides(rect, collision_matrix):
            if self.direction.x > 0:
                rect.right = (rect.right // TILE_SIZE) * TILE_SIZE
            elif self.direction.x < 0:
                rect.left = (rect.left // TILE_SIZE + 1) * TILE_SIZE

        # Trục Y
        rect.y += self.direction.y * self.speed * dt
        if self.collides(rect, collision_matrix):
            if self.direction.y > 0:
                rect.bottom = (rect.bottom // TILE_SIZE) * TILE_SIZE
            elif self.direction.y < 0:
                rect.top = (rect.top // TILE_SIZE + 1) * TILE_SIZE

        # --- Gán lại vị trí thực tế ---
        self.rect.x = rect.x + self.offset_x
        self.rect.y = rect.y + self.offset_y

    def collides(self, rect, collision_matrix):
        rows, cols = collision_matrix.shape
        left = rect.left // TILE_SIZE
        right = (rect.right - 1) // TILE_SIZE
        top = rect.top // TILE_SIZE
        bottom = (rect.bottom - 1) // TILE_SIZE

        for y in range(top, bottom + 1):
            for x in range(left, right + 1):
                if 0 <= x < cols and 0 <= y < rows:
                    if collision_matrix[y][x] == 1:
                        return True
        return False

    def animate(self, dt):
        """Cập nhật animation dựa trên self.state, không phụ thuộc bàn phím."""
        frames = self.animations[self.state]
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speeds[self.state]:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(frames)

        frame = frames[self.frame_index]
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)
        self.image = frame
        
    def set_state(self, state, facing=None):
        """Cập nhật trạng thái idle/run và hướng nếu có."""
        if state in ("idle", "run"):
            self.state = state
        if facing is not None:
            self.facing_right = facing



class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.sheet = pygame.image.load("Resources/Characters/run_red.png").convert_alpha()
        self.frame_w, self.frame_h = 96, 96
        self.frame_count = 6
        self.frames = [
            pygame.transform.scale(
                self.sheet.subsurface(pygame.Rect(i * self.frame_w, 0, self.frame_w, self.frame_h)), (64, 64)
            )
            for i in range(self.frame_count)
        ]
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)
        self.frame_index = 0
        self.timer = 0
        self.animation_speed = 0.1
        self.facing_right = True

    def update(self, dt, start_pos, end_pos, t):
        # --- Di chuyển mượt ---
        x = start_pos[0] + (end_pos[0] - start_pos[0]) * t
        y = start_pos[1] + (end_pos[1] - start_pos[1]) * t
        self.rect.center = (x, y)

        # --- Cập nhật hướng ---
        self.facing_right = end_pos[0] >= start_pos[0]

        # --- Cập nhật frame ---
        self.timer += dt
        if self.timer >= self.animation_speed:
            self.timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
        frame = self.frames[self.frame_index]
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)
        self.image = frame

