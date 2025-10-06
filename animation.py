import pygame

class SpriteSheetAnimation:
    def __init__(self, image_path, frame_width, frame_height, frame_count, fps=10, loop=True):
        """
        image_path   : đường dẫn đến sprite sheet
        frame_width  : chiều rộng 1 frame
        frame_height : chiều cao 1 frame
        frame_count  : số lượng frame trong sheet
        fps          : tốc độ chuyển frame
        loop         : True nếu muốn lặp lại
        """
        self.sheet = pygame.image.load(image_path).convert_alpha()
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frame_count = frame_count
        self.fps = fps
        self.loop = loop

        self.frames = []
        for i in range(frame_count):
            rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            frame = self.sheet.subsurface(rect)
            self.frames.append(frame)

        self.current_frame = 0
        self.timer = 0
        self.finished = False

    def update(self, dt):
        """Cập nhật frame theo thời gian (dt = delta time tính bằng giây)."""
        if self.finished:
            return

        self.timer += dt
        if self.timer >= 1 / self.fps:
            self.timer = 0
            self.current_frame += 1

            if self.current_frame >= self.frame_count:
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = self.frame_count - 1
                    self.finished = True

    def draw(self, surface, pos, scale=1.0, flip=False):
        """Vẽ frame hiện tại lên surface tại vị trí pos."""
        frame = self.frames[self.current_frame]
        if scale != 1.0:
            frame = pygame.transform.scale(frame, 
                                           (int(self.frame_width * scale), int(self.frame_height * scale)))
        if flip:
            frame = pygame.transform.flip(frame, True, False)
        rect = frame.get_rect(center=pos)
        surface.blit(frame, rect)
