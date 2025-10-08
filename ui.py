import pygame

class UIManager:
    def __init__(self, font=None):
        if font is None:
            self.font = pygame.font.Font("Resources/Font/pixel3.ttf", 23)
        else:
            self.font = font
        self.panel_img = pygame.image.load("Resources/Menu/panel.png").convert_alpha()

    def draw_text(self, surface, text, x, y, color=(0,0,0), pathFont=None, size=16):
        if pathFont:
            font = pygame.font.Font(pathFont, size)
        else:
            font = self.font
        txt_surf = font.render(text, False, color)
        surface.blit(txt_surf, (x, y))


    def draw_panel(self, surface, x, y, width, height, title=None, img_panel=None):
        if img_panel:
            panel_scaled = pygame.transform.scale(img_panel, (width, height))
            surface.blit(panel_scaled, (x, y))
        else:
            panel_scaled = pygame.transform.scale(self.panel_img, (width, height))
            surface.blit(panel_scaled, (x, y))
        if title:
            self.draw_text(surface, title, x + 35, y + 20)
        return pygame.Rect(x, y, width, height)

    def draw_dropmenu(self, surface, x, y, width, height, options, state, mouse_pos, mouse_click):
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, (240, 240, 240), rect)
        pygame.draw.rect(surface, (0, 0, 0), rect, 2)

        if state["selected"]:
            txt = self.font.render(state["selected"], False, (0,0,0))
            surface.blit(txt, (x+5, y+5))

        if mouse_click and rect.collidepoint(mouse_pos):
            state["open"] = not state["open"]

        chosen = None
        if state["open"]:
            for i, opt in enumerate(options):
                r = pygame.Rect(x, y + (i+1)*height, width, height)
                pygame.draw.rect(surface, (255,255,255), r)
                pygame.draw.rect(surface, (0,0,0), r, 1)
                txt = self.font.render(opt, False, (0,0,0))
                surface.blit(txt, (r.x+5, r.y+5))

                if mouse_click and r.collidepoint(mouse_pos):
                    state["selected"] = opt
                    state["open"] = False
                    chosen = opt
        return chosen

    def draw_image_button(self, surface, x, y,
                        img_normal, img_hover, img_pressed,
                        mouse_pos, mouse_click,
                        widthscale=1.0, heightscale=1.0,
                        text=None,
                        text_normal=(255, 255, 255),
                        text_hover=(255, 255, 0),
                        text_pressed=(255, 255, 255)):
        # scale ảnh
        w = int(img_normal.get_width() * widthscale)
        h = int(img_normal.get_height() * heightscale)

        normal_scaled = pygame.transform.scale(img_normal, (w, h))
        hover_scaled = pygame.transform.scale(img_hover, (w, h))
        pressed_scaled = pygame.transform.scale(img_pressed, (w, h))

        rect = pygame.Rect(x, y, w, h)

        # chọn ảnh + màu chữ theo trạng thái
        if rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:  # đang giữ chuột
                surface.blit(pressed_scaled, (x, y))
                text_color = text_pressed
            else:  # hover
                surface.blit(hover_scaled, (x, y))
                text_color = text_hover
        else:
            surface.blit(normal_scaled, (x, y))
            text_color = text_normal

        # vẽ chữ vào giữa button
        if text:
            text_surf = self.font.render(text, True, text_color)
            surface.blit(text_surf, (
                rect.centerx - text_surf.get_width() // 2,
                rect.centery - text_surf.get_height() // 1   
            ))

        # click thực sự
        if mouse_click and rect.collidepoint(mouse_pos):
            return True
        return False

    
