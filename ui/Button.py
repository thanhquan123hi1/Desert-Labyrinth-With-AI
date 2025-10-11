import pygame


class Button:
    def __init__(self, x, y, w, h, text, font, color, hover_color, text_color=(255,255,255)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (255,255,255), self.rect, 2)

        txt = self.font.render(self.text, True, self.text_color)
        surface.blit(txt, (self.rect.x + (self.rect.width - txt.get_width())//2,
                           self.rect.y + (self.rect.height - txt.get_height())//2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
