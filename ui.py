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


    def draw_panel(self, surface, x, y, width, height, title=None, panel_img=None):
        if panel_img:
            panel_scaled = pygame.transform.scale(panel_img, (width, height))
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

    

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Demo UI Manager")

    ui = UIManager(pygame.font.SysFont("Arial", 20))
    drop_state = {"open": False, "selected": "BFS"}
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        mouse_pressed = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = True

        screen.fill((255, 255, 255))

        # Panel
        ui.draw_panel(screen, 50, 50, 500, 400, "Control Panel")

        # Normal button
        if ui.draw_button(screen, 70, 100, 120, 40, "Run", mouse_pos, mouse_click):
            print("Run clicked")
        # Dropmenu
        selected = ui.draw_dropmenu(screen, 70, 160, 150, 30,
                                    ["BFS", "DFS", "A*"], drop_state,
                                    mouse_pos, mouse_click)
        if selected:
            print("Selected:", selected)



        pygame.display.flip()
    pygame.quit()
