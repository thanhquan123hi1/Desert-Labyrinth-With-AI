import pygame, sys
from animation import SpriteSheetAnimation
from ui import UIManager

class Options:
    def __init__(self, screen):
        self.screen = screen
        self.ui = UIManager()
        self.clock = pygame.time.Clock()
        self.bg = pygame.image.load("Resources/Maps/desert.png").convert()
        self.panel_img = pygame.image.load("Resources/Menu/option_panel.png").convert_alpha()

        # back button
        self.imgNormal_back = pygame.image.load("Resources/Maps/buttons/back_normal.png").convert_alpha()
        self.imgHover_back = pygame.image.load("Resources/Maps/buttons/back_hover.png").convert_alpha()
        self.imgPressed_back = pygame.image.load("Resources/Maps/buttons/back_pressed.png").convert_alpha()

        # Tạo animation mũi tên từ cùng một sheet
        self.arrow_anim = SpriteSheetAnimation(
            "Resources/Animation/sheetarrow.png",
            frame_width=128,
            frame_height=128,
            frame_count=7,
            fps=15,
            loop=True
        )

    def draw(self):
            self.ui.draw_panel(self.screen, 370,30,704,480, panel_img=self.panel_img)


    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            mouse_click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_click = True

            # Cập nhật animation
            self.arrow_anim.update(dt)

            # Vẽ nền
            self.screen.blit(self.bg, (0, 0))
            if self.ui.draw_image_button(self.screen, 0, 0, 
                            self.imgNormal_back, self.imgHover_back, self.imgPressed_back ,mouse_pos, mouse_click, 1.2, 1.2):
                return "BACK"
            
            self.draw()

            # Vẽ mũi tên trái (flip=True để lật ngang)
            self.arrow_anim.draw(self.screen, (50, 400), scale=0.6, flip=True)

            # Vẽ mũi tên phải (flip=False giữ nguyên)
            self.arrow_anim.draw(self.screen, (1400, 400), scale=0.6, flip=False)

            pygame.display.flip()
