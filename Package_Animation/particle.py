import pygame, random, math
from settings import RES

class Particles:
    def __init__(self, num_particles=80):
        self.num_particles = num_particles
        self.reset_particles()
        self.wind = 0
        self.lightning_timer = 0
        self.lightning_alpha = 0  

        # Lớp tuyết tích tụ
        self.snow_ground = pygame.Surface(RES, pygame.SRCALPHA)
        self.ground_level = RES[1] - 50  

        # splash (cho mưa)
        self.splashes = []

    def reset_particles(self):
        """Khởi tạo lại các hạt"""
        self.particles = [
            [random.randint(0, RES[0]), random.randint(0, RES[1]),
             random.uniform(0.5, 2.0), random.randint(2, 5)]  # x,y,speed,size
            for _ in range(self.num_particles)
        ]

    def update_wind(self):
        """Tính sức gió dao động"""
        ticks = pygame.time.get_ticks() * 0.001
        self.wind = math.sin(ticks * 0.5) * 1.2

    # Sa mạc: mặt trời + hạt cát + sóng cát
    def desertEffect(self, screen):
        sun_center = (RES[0] - 120, 100)
        for r, alpha in [(80, 30), (60, 60), (40, 120)]:
            surface = pygame.Surface(RES, pygame.SRCALPHA)
            pygame.draw.circle(surface, (255, 230, 120, alpha), sun_center, r)
            screen.blit(surface, (0, 0))
        pygame.draw.circle(screen, (255, 220, 100), sun_center, 30)

        # cát bay ngang
        for p in self.particles:
            x, y, speed, size = p
            pygame.draw.circle(screen, (230, 200, 140), (int(x), int(y)), size)
            p[0] += speed
            if p[0] > RES[0]:
                p[0] = -size
                p[1] = random.randint(0, RES[1])
                p[2] = random.uniform(0.5, 2.0)

        # sóng cát
        ticks = pygame.time.get_ticks() * 0.002
        base_y = RES[1] - 100
        for y in range(base_y, RES[1], 8):
            points = [(x, y + int(10 * math.sin(x * 0.05 + ticks + y * 0.1)))
                      for x in range(0, RES[0] + 20, 20)]
            pygame.draw.lines(screen, (220, 180, 120), False, points, 2)

    # Tuyết rơi + tích tụ
    def snowEffect(self, screen):
        self.update_wind()

        for p in self.particles:
            x, y, speed, size = p
            pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), size)

            # di chuyển
            p[0] += self.wind * (size * 0.2) + speed * 0.2
            p[1] += speed * (0.5 + size * 0.2)

            # chạm đất → vẽ vào snow_ground
            if p[1] >= self.ground_level:
                gx, gy = int(p[0]), int(self.ground_level + random.randint(-2, 2))
                if 0 <= gx < RES[0]:
                    pygame.draw.circle(self.snow_ground, (255, 255, 255, 220), (gx, gy), size//2 + 1)
                # reset hạt
                p[1] = -size
                p[0] = random.randint(0, RES[0])
                p[2] = random.uniform(0.5, 2.0)

        # vẽ lớp tuyết đã tích tụ
        screen.blit(self.snow_ground, (0, 0))

    # Mưa + splash + phản chiếu + sấm sét
    def rainEffect(self, screen):
        self.update_wind()

        # --- vẽ hạt mưa ---
        for p in self.particles:
            x, y, speed, size = p
            pygame.draw.line(screen, (150, 150, 255),
                             (int(x), int(y)),
                             (int(x + self.wind * 2), int(y + size * 6)), 1)

            # di chuyển
            p[0] += self.wind * (0.5 + size * 0.1)
            p[1] += speed * (4 + size * 0.5)

            # chạm đất → splash
            if p[1] >= RES[1] - 5:
                self.splashes.append([x, RES[1] - 5, 2, 180])  # (x,y,radius,alpha)
                p[1] = -size
                p[0] = random.randint(0, RES[0])
                p[2] = random.uniform(0.5, 2.0)

        # --- vẽ splash ---
        for s in self.splashes[:]:
            x, y, r, a = s
            surf = pygame.Surface(RES, pygame.SRCALPHA)
            pygame.draw.circle(surf, (180, 180, 255, a), (int(x), int(y)), r, 1)
            screen.blit(surf, (0, 0))
            s[2] += 1   # radius tăng
            s[3] -= 15  # alpha giảm
            if s[3] <= 0:
                self.splashes.remove(s)

        # --- phản chiếu đất ướt ---
        ground_overlay = pygame.Surface((RES[0], 80), pygame.SRCALPHA)
        ground_overlay.fill((50, 50, 80, 60))
        screen.blit(ground_overlay, (0, RES[1] - 80))

        # --- sấm sét ---
        self.handle_lightning(screen)

    # Sấm sét lóe sáng + tia sét ngoằn ngoèo
    def handle_lightning(self, screen):
        if self.lightning_timer <= 0 and random.random() < 0.005:
            self.lightning_timer = random.randint(2, 6)
            self.lightning_alpha = 200

        if self.lightning_timer > 0:
            overlay = pygame.Surface(RES, pygame.SRCALPHA)
            overlay.fill((255, 255, 255, self.lightning_alpha))
            screen.blit(overlay, (0, 0))
            self.lightning_alpha = max(0, self.lightning_alpha - 50)
            self.lightning_timer -= 1

            # vẽ tia sét
            start_x = random.randint(RES[0]//3, RES[0] - RES[0]//3)
            y = 0
            for _ in range(random.randint(3, 5)):
                end_x = start_x + random.randint(-20, 20)
                end_y = y + random.randint(40, 80)
                pygame.draw.line(screen, (255, 255, 255), (start_x, y), (end_x, end_y), 2)
                start_x, y = end_x, end_y
    # Bão cát
    def sandstormEffect(self, screen):
        self.update_wind()
        overlay = pygame.Surface(RES, pygame.SRCALPHA)

        for p in self.particles:
            x, y, speed, size = p
            color = (220+random.randint(-10,10), 200, 140, 180)
            pygame.draw.circle(overlay, color, (int(x), int(y)), size)
            p[0] += speed*2 + self.wind*2
            p[1] += random.uniform(-0.3, 0.3)
            if p[0] > RES[0] or p[1] > RES[1] or p[1] < 0:
                p[0] = -size
                p[1] = random.randint(0, RES[1])
                p[2] = random.uniform(0.5, 2.0)

        screen.blit(overlay, (0,0), special_flags=pygame.BLEND_RGBA_ADD)

    # Đom đóm
    def firefliesEffect(self, screen):
        if not hasattr(self, "fireflies"):
            self.fireflies = [
                [random.randint(0, RES[0]), random.randint(0, RES[1]),
                 random.uniform(0.5, 1.5), random.random()*math.pi*2]  # x,y,speed,phase
                for _ in range(20)
            ]

        ticks = pygame.time.get_ticks() * 0.005
        for f in self.fireflies:
            x, y, speed, phase = f
            glow = int(150 + 105*math.sin(ticks + phase))  # nhấp nháy
            color = (200, 255, 150, glow)

            surf = pygame.Surface((8,8), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (4,4), 3)
            screen.blit(surf, (x, y))

            # di chuyển lượn sóng
            f[0] += math.sin(ticks + phase) * 0.5
            f[1] += math.cos(ticks*0.3 + phase) * 0.2

            # giữ trong màn hình
            if f[0] < 0: f[0] = RES[0]
            if f[0] > RES[0]: f[0] = 0
            if f[1] < 0: f[1] = RES[1]
            if f[1] > RES[1]: f[1] = 0

    # Lá rơi
    def leavesEffect(self, screen):
        if not hasattr(self, "leaves"):
            self.leaves = [
                [random.randint(0, RES[0]), random.randint(-RES[1], 0),
                 random.uniform(1, 2), random.randint(20, 40), 0]  # x,y,speed,rotate_speed,angle
                for _ in range(25)
            ]

        for leaf in self.leaves:
            x, y, speed, rotate_speed, angle = leaf
            angle += rotate_speed * 0.01
            leaf[4] = angle
            leaf[0] += self.wind*0.5 + math.sin(angle)*1.5
            leaf[1] += speed

            # vẽ lá (ellipse xoay)
            surf = pygame.Surface((20, 10), pygame.SRCALPHA)
            pygame.draw.ellipse(surf, (180, 120, 50), (0,0,20,10))
            surf = pygame.transform.rotate(surf, math.degrees(angle))
            rect = surf.get_rect(center=(int(leaf[0]), int(leaf[1])))
            screen.blit(surf, rect)

            # reset khi rơi khỏi màn hình
            if leaf[1] > RES[1]:
                leaf[0] = random.randint(0, RES[0])
                leaf[1] = random.randint(-100, -20)
                leaf[2] = random.uniform(1,2)
                leaf[3] = random.randint(20,40)
                leaf[4] = 0
    # ================================================
    # Hiệu ứng bụi khi player bước đi
    def playerStepEffect(self, pos):
        """Tạo bụi nhỏ tại vị trí bước chân player"""
        if not hasattr(self, "player_dust"):
            self.player_dust = []
        for _ in range(random.randint(3, 6)):
            x, y = pos
            vx = random.uniform(-1.0, 1.0)
            vy = random.uniform(-2.0, -0.5)
            size = random.randint(2, 4)
            life = 1.0
            self.player_dust.append([x, y, vx, vy, size, life])

    def update_player_dust(self, screen, dt):
        """Cập nhật và vẽ bụi chân player"""
        if not hasattr(self, "player_dust"):
            return
        alive = []
        for d in self.player_dust:
            x, y, vx, vy, size, life = d
            x += vx
            y += vy
            vy += 0.1
            life -= dt * 1.5
            if life > 0:
                alpha = int(255 * life)
                color = (230, 200, 120, alpha)
                s = pygame.Surface((size, size), pygame.SRCALPHA)
                s.fill(color)
                screen.blit(s, (x, y))
                alive.append([x, y, vx, vy, size, life])
        self.player_dust = alive
