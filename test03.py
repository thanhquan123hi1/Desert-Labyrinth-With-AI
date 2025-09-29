import pygame, sys, random

pygame.init()
WIDTH, HEIGHT = 1312, 736
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu with Shooting Stars + Moving Clouds")

clock = pygame.time.Clock()

# Load background
bg = pygame.image.load("Resources/Menu/bgsky.png").convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# Load mây
cloud1 = pygame.image.load("Resources/Menu/cloud1.png").convert_alpha()
cloud2 = pygame.image.load("Resources/Menu/cloud2.png").convert_alpha()

# Scale mây cho vừa
cloud1 = pygame.transform.scale(cloud1, (300, 300))
cloud2 = pygame.transform.scale(cloud2, (300, 300))

# Vị trí ban đầu của mây
clouds = [
    [200, 100, 1, cloud1],  # [x, y, speed, image]
    [600, 200, 0.5, cloud2]
]

# Danh sách sao: [x, y, dx, dy, trail]
stars = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    # --- Vẽ nền ---
    screen.blit(bg, (0, 0))

    # --- Cập nhật & vẽ mây ---
    for cloud in clouds:
        cloud[0] += cloud[2]  # di chuyển ngang
        if cloud[0] > WIDTH:  # nếu ra khỏi màn hình thì quay lại từ bên trái
            cloud[0] = -cloud[3].get_width()
            cloud[1] = random.randint(50, HEIGHT // 2)  # random lại cao độ
        screen.blit(cloud[3], (int(cloud[0]), int(cloud[1])))

    # --- Tạo sao mới ---
    if random.randint(0, 80) == 0:
        x = random.randint(0, WIDTH // 2)
        y = random.randint(0, HEIGHT // 2)
        dx = random.uniform(5, 8)
        dy = random.uniform(3, 6)
        stars.append([x, y, dx, dy, []])

    # --- Cập nhật & vẽ sao ---
    for star in stars[:]:
        x, y, dx, dy, trail = star
        x += dx
        y += dy
        trail.append((x, y))
        if len(trail) > 15:
            trail.pop(0)

        for i, (tx, ty) in enumerate(trail):
            alpha = int(255 * (i + 1) / len(trail))
            color = (255, 255, 200, alpha)
            surf = pygame.Surface((4, 4), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (2, 2), 2)
            screen.blit(surf, (int(tx), int(ty)))

        star[0], star[1], star[4] = x, y, trail
        if x > WIDTH or y > HEIGHT:
            stars.remove(star)

    pygame.display.flip()
    clock.tick(60)
