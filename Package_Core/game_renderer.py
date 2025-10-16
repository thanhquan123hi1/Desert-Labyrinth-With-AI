import pygame, math
from settings import TILE_SIZE
from Package_Animation import SpriteSheetAnimation


class GameRenderer:
    def __init__(self, surface, map_model, player, goals,
                 map_offset=(32, 32), particles=None, effect_name="baocat"):
        self.surface = surface
        self.map_model = map_model
        self.player = player
        self.offset = map_offset
        self.particles = particles
        self.effect_name = effect_name
        self.player_group = pygame.sprite.GroupSingle(player)

        # --- Chuẩn hóa goals ---
        if isinstance(goals, (tuple, list)) and isinstance(goals[0], int):
            self.goals = [goals]
        else:
            self.goals = list(goals)

        self.goal_anim = SpriteSheetAnimation(
            image_path="Resources/Animation/goal.png",
            frame_width=32, frame_height=32,
            frame_count=8, fps=8, loop=True
        )

        # --- Hiệu ứng ---
        self.visited_age = {}
        self.path_phase = 0.0

        # --- Chế độ Adversarial ---
        self.is_adversarial = False
        self.adv_player_path = []
        self.adv_enemy_path = []
        self.adv_step = 0.0
        self.adv_speed = 0.15
        
        self.enemy_pos = None
        self.enemy_pixel = None
        self.enemy_sprite = None
        self.enemy_group = None


    # ==========================================================
    def set_adversarial(self, player_path=None, enemy_path=None):
        """Kích hoạt chế độ Adversarial"""
        self.is_adversarial = True
        self.adv_player_path = list(player_path) if player_path else []
        self.adv_enemy_path = list(enemy_path) if enemy_path else []
        self.adv_step = 0.0

    def disable_adversarial(self):
        """Tắt chế độ Adversarial"""
        self.is_adversarial = False
        self.adv_player_path.clear()
        self.adv_enemy_path.clear()

    # ==========================================================
    def draw(self, dt, visible_visited, visible_path):
        self.map_model.update(dt)
        self.map_model.draw(self.surface)
        colors = self.get_theme_colors(self.effect_name)

        # Chỉ vẽ glow nếu KHÔNG ở chế độ adversarial
        if not self.is_adversarial:
            if visible_visited:
                self.draw_cells_energy(visible_visited, base_color=colors["visited"])
            if visible_path:
                self.path_phase += dt * 4.0
                self.draw_cells_pathpulse(visible_path, self.path_phase, base_color=colors["path"])

        # --- Vẽ đích ---
        self.goal_anim.update(dt)
        for (r, c) in self.goals:
            pos = (self.offset[0] + c * TILE_SIZE + TILE_SIZE // 2,
                   self.offset[1] + r * TILE_SIZE + TILE_SIZE // 2)
            self.goal_anim.draw(self.surface, pos, scale=1.0)

        # --- Nếu là adversarial ---
        if self.is_adversarial and (self.adv_player_path or self.adv_enemy_path):
            self.draw_adversarial(dt)
            # Vẽ player và enemy sprite
            if hasattr(self, "player") and self.player:
                self.surface.blit(self.player.image, self.player.rect)
            if self.enemy_sprite:
                self.surface.blit(self.enemy_sprite.image, self.enemy_sprite.rect)
        else:
            self.player.update(dt, self.map_model.collision_matrix)
            self.player_group.draw(self.surface)


    # ==========================================================
    def draw_adversarial(self, dt):
        """Vẽ Player & Enemy bằng sprite animation (chuẩn, mượt, flip hướng)"""
        if not self.adv_player_path:
            return

        self.adv_step += dt / self.adv_speed
        idx = int(self.adv_step)
        if idx >= len(self.adv_player_path) - 1:
            # Nếu player tới đích
            final_r, final_c = self.adv_player_path[-1]
            self.player.rect.center = (
                self.offset[0] + final_c * TILE_SIZE + TILE_SIZE // 2,
                self.offset[1] + final_r * TILE_SIZE + TILE_SIZE // 2,
            )
            self.player.state = "idle"
            if self.enemy_sprite:
                # Giữ enemy tại frame cuối, không biến mất
                er, ec = self.adv_enemy_path[-1]
                self.enemy_sprite.rect.center = (
                    self.offset[0] + ec * TILE_SIZE + TILE_SIZE // 2,
                    self.offset[1] + er * TILE_SIZE + TILE_SIZE // 2,
                )
            return

        t = self.adv_step - idx

        # --- Player ---
        pr1, pc1 = self.adv_player_path[idx]
        pr2, pc2 = self.adv_player_path[idx + 1]
        start_p = (
            self.offset[0] + pc1 * TILE_SIZE + TILE_SIZE // 2,
            self.offset[1] + pr1 * TILE_SIZE + TILE_SIZE // 2,
        )
        end_p = (
            self.offset[0] + pc2 * TILE_SIZE + TILE_SIZE // 2,
            self.offset[1] + pr2 * TILE_SIZE + TILE_SIZE // 2,
        )

        self.player.rect.center = (
            start_p[0] + (end_p[0] - start_p[0]) * t,
            start_p[1] + (end_p[1] - start_p[1]) * t,
        )
        # Xác định hướng dựa theo tọa độ di chuyển
        facing_right = end_p[0] >= start_p[0]
        self.player.set_state("run", facing=facing_right)
        self.player.animate(dt)

        # --- Enemy ---
        if self.adv_enemy_path and idx < len(self.adv_enemy_path) - 1:
            er1, ec1 = self.adv_enemy_path[idx]
            er2, ec2 = self.adv_enemy_path[idx + 1]
            start_e = (
                self.offset[0] + ec1 * TILE_SIZE + TILE_SIZE // 2,
                self.offset[1] + er1 * TILE_SIZE + TILE_SIZE // 2,
            )
            end_e = (
                self.offset[0] + ec2 * TILE_SIZE + TILE_SIZE // 2,
                self.offset[1] + er2 * TILE_SIZE + TILE_SIZE // 2,
            )
            if self.enemy_sprite:
                self.enemy_sprite.update(dt, start_e, end_e, t)

        # --- Vẽ đường đi ---
        if len(self.adv_player_path) > 1:
            pts_p = [(self.offset[0] + c * TILE_SIZE + TILE_SIZE // 2,
                    self.offset[1] + r * TILE_SIZE + TILE_SIZE // 2)
                    for r, c in self.adv_player_path]
            pygame.draw.lines(self.surface, (200, 255, 255), False, pts_p, 2)
        if len(self.adv_enemy_path) > 1:
            pts_e = [(self.offset[0] + c * TILE_SIZE + TILE_SIZE // 2,
                    self.offset[1] + r * TILE_SIZE + TILE_SIZE // 2)
                    for r, c in self.adv_enemy_path]
            pygame.draw.lines(self.surface, (255, 80, 80), False, pts_e, 2)

        # --- Vẽ sprite ---
        self.surface.blit(self.player.image, self.player.rect)
        if self.enemy_sprite:
            self.surface.blit(self.enemy_sprite.image, self.enemy_sprite.rect)



    # ==========================================================
    def draw_cells_energy(self, cells, base_color=(80, 200, 255)):
        """Hiệu ứng năng lượng lan tỏa ở visited."""
        now = pygame.time.get_ticks() / 1000.0
        for cell in cells:
            items = cell if isinstance(cell, (set, frozenset, list)) else [cell]
            for (r, c) in items:
                key = (r, c)
                if key not in self.visited_age:
                    self.visited_age[key] = now
                age = now - self.visited_age[key]
                pulse = 0.5 + 0.5 * math.sin(age * 10)
                alpha = int(180 * math.exp(-2 * age) * pulse)
                color = (*base_color, max(50, alpha))
                self._draw_single(r, c, color)

    # =====================================================================
    def draw_cells_pathpulse(self, cells, phase, base_color=(0, 255, 255)):
        """Đường cyan có ánh sáng chạy."""
        for idx, item in enumerate(cells):
            items = item if isinstance(item, (set, frozenset, list)) else [item]
            for (r, c) in items:
                glow = 0.5 + 0.5 * math.sin(phase * 2 + idx * 0.5)
                color = (
                    int(base_color[0] * (0.7 + 0.3 * glow)),
                    int(base_color[1] * (0.7 + 0.3 * glow)),
                    int(base_color[2] * (0.7 + 0.3 * glow)),
                    160,
                )
                self._draw_single(r, c, color)

    def _draw_single(self, r, c, color):
        rect = pygame.Rect(
            c * TILE_SIZE + self.offset[0],
            r * TILE_SIZE + self.offset[1],
            TILE_SIZE, TILE_SIZE
        )
        s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        s.fill(color)
        self.surface.blit(s, rect.topleft)

    def get_theme_colors(self, effect_name):
        themes = {
            "baocat": {"visited": (255, 140, 30), "path": (255, 170, 60), "goal": (255, 210, 80)},
            "snow": {"visited": (130, 190, 255), "path": (150, 220, 255), "goal": (255, 255, 255)},
            "leaves": {"visited": (60, 170, 60), "path": (80, 200, 80), "goal": (180, 255, 180)},
            "rain": {"visited": (40, 110, 220), "path": (60, 140, 255), "goal": (200, 220, 255)},
            "fireflies": {"visited": (255, 200, 70), "path": (220, 200, 80), "goal": (255, 255, 180)},
        }
        return themes.get(effect_name, themes["baocat"])

    def reset_effects(self):
        self.visited_age.clear()
        self.path_phase = 0.0
        self.disable_adversarial()
        
        
    def draw_enemy_marker(self):
        """Vẽ enemy (ký hiệu tạm)"""
        if not self.enemy_pos:
            return
        r, c = self.enemy_pos
        x = self.offset[0] + c * TILE_SIZE + TILE_SIZE // 2
        y = self.offset[1] + r * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(self.surface, (255, 50, 50), (int(x), int(y)), TILE_SIZE // 3)
        font = pygame.font.Font(None, 20)
        e_text = font.render("E", True, (0, 0, 0))
        self.surface.blit(e_text, (x - 6, y - 8))
        
    def draw_enemy_sprite(self):
        """Vẽ enemy nếu có sprite"""
        if hasattr(self, "enemy_sprite") and self.enemy_sprite:
            self.surface.blit(self.enemy_sprite.image, self.enemy_sprite.rect)
