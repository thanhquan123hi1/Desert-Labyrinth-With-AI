import pygame, sys

pygame.init()
screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("23110145 - Environment Effects")
clock = pygame.time.Clock()

# --- Load hình ---
panel_img = pygame.image.load("Resources/Menu/envir.png").convert_alpha()
effects = [
    ("Bão cát", pygame.image.load("Resources/Menu/envir/baocat.png").convert_alpha()),
    ("Đom đóm", pygame.image.load("Resources/Menu/envir/domdom.png").convert_alpha()),
    ("Lá rơi", pygame.image.load("Resources/Menu/envir/leaves.png").convert_alpha()),
    ("Mưa", pygame.image.load("Resources/Menu/envir/rain.png").convert_alpha()),
    ("Tuyết", pygame.image.load("Resources/Menu/envir/snow.png").convert_alpha()),
]

effects = [(name, pygame.transform.smoothscale(img, (90, 90))) for name, img in effects]
font = pygame.font.Font(None, 32)

# -----------------------------------------------------
def draw_effect_panel(surface, x, y, title_img, icons, selected_idx=None, hover_idx=None):
    """Vẽ panel chứa danh sách hiệu ứng"""
    surface.blit(title_img, (x, y))
    panel_rect = pygame.Rect(x, y, title_img.get_width(), title_img.get_height())

    # --- căn giữa các icon ---
    icon_w = icons[0][1].get_width()
    padding = 40
    total_width = len(icons) * icon_w + (len(icons) - 1) * padding
    start_x = panel_rect.centerx - total_width // 2
    y_icons = panel_rect.centery - 30

    icon_rects = []
    for i, (name, img) in enumerate(icons):
        x_icon = start_x + i * (icon_w + padding)
        rect = pygame.Rect(x_icon, y_icons, icon_w, icon_w)
        icon_rects.append(rect)

        # viền nền nhẹ
        bg_rect = rect.inflate(14, 14)
        pygame.draw.rect(surface, (240, 220, 180), bg_rect, border_radius=12)

        surface.blit(img, rect.topleft)

        # viền chọn
        if selected_idx == i:
            pygame.draw.rect(surface, (255, 255, 0), bg_rect, 5, border_radius=12)
        elif hover_idx == i:
            pygame.draw.rect(surface, (255, 255, 150), bg_rect, 3, border_radius=12)
        else:
            pygame.draw.rect(surface, (100, 80, 50), bg_rect, 2, border_radius=12)

        # nếu hover, hiển thị tên hiệu ứng bên dưới
        if hover_idx == i:
            text = font.render(name, True, (50, 30, 10))
            text_rect = text.get_rect(center=(rect.centerx, rect.bottom + 25))
            surface.blit(text, text_rect)

    return icon_rects

# -----------------------------------------------------
selected = None
hovered = None

while True:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, r in enumerate(icon_rects):
                if r.collidepoint(mouse_pos):
                    selected = i

    screen.fill((210, 180, 120))  # nền cát

    # cập nhật hover icon
    hovered = None
    for i, r in enumerate(effects):
        if i < len(effects) and 'icon_rects' in locals():
            if icon_rects[i].collidepoint(mouse_pos):
                hovered = i

    # vẽ panel
    icon_rects = draw_effect_panel(screen, 90, 100, panel_img, effects, selected, hovered)

    pygame.display.flip()
    clock.tick(60)
