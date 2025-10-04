import pygame, sys

# 2: vị trí nhân vật
# 3: vị trí goal

class Dropdown:
    def __init__(self, x, y, w, h, font, main_color, highlight_color, options):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.main_color = main_color
        self.highlight_color = highlight_color
        self.options = options
        self.active_option = options[0]  # mặc định chọn cái đầu
        self.show_menu = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.main_color, self.rect)
        pygame.draw.rect(surface, (255,255,255), self.rect, 2)
        txt = self.font.render(self.active_option, True, (255,255,255))
        surface.blit(txt, (self.rect.x+5, self.rect.y+5))

        if self.show_menu:
            for i, option in enumerate(self.options):
                rect = pygame.Rect(self.rect.x, self.rect.y + (i+1)*self.rect.height,
                                   self.rect.width, self.rect.height)
                pygame.draw.rect(surface, self.main_color, rect)
                pygame.draw.rect(surface, (255,255,255), rect, 2)
                txt = self.font.render(option, True, (255,255,255))
                surface.blit(txt, (rect.x+5, rect.y+5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.show_menu = not self.show_menu
            elif self.show_menu:
                for i, option in enumerate(self.options):
                    rect = pygame.Rect(self.rect.x, self.rect.y + (i+1)*self.rect.height,
                                       self.rect.width, self.rect.height)
                    if rect.collidepoint(event.pos):
                        self.active_option = option
                        self.show_menu = False
                        return option
                self.show_menu = False
        return None