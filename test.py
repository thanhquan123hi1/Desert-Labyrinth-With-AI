import pygame, sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
clock = pygame.time.Clock()

def draw_inner_shadow(surface, thickness=20):
    shadow = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for i in range(thickness):
        # Giảm dần độ mờ từ ngoài vào trong
        alpha = int(180 * (1 - i / thickness))
        # Vẽ hình chữ nhật co dần vào
        pygame.draw.rect(
            shadow,
            (0, 0, 0, alpha),
            (i, i, WIDTH - 2*i, HEIGHT - 2*i),
            width=3  # độ dày mỗi vòng
        )
    surface.blit(shadow, (0, 0))

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((50, 80, 130))  # màu nền
    draw_inner_shadow(screen)
    pygame.display.flip()
    clock.tick(60)
