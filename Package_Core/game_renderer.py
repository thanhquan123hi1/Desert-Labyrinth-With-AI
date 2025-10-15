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
        else:
            self.player.update(dt, self.map_model.collision_matrix)
            self.player_group.draw(self.surface)

    # ==========================================================
    def draw_adversarial(self, dt):
        """Vẽ Player & Enemy cùng di chuyển (không glow)"""
        if not self.adv_player_path:
            return

        self.adv_step += dt / self.adv_speed
        idx = int(self.adv_step)
        idx = min(idx, len(self.adv_player_path) - 1)
        idx_enemy = min(idx, len(self.adv_enemy_path) - 1) if self.adv_enemy_path else idx

        pr, pc = self.adv_player_path[idx]
        px = self.offset[0] + pc * TILE_SIZE + TILE_SIZE // 2
        py = self.offset[1] + pr * TILE_SIZE + TILE_SIZE // 2

        er, ec = self.adv_enemy_path[idx_enemy] if self.adv_enemy_path else (pr, pc)
        ex = self.offset[0] + ec * TILE_SIZE + TILE_SIZE // 2
        ey = self.offset[1] + er * TILE_SIZE + TILE_SIZE // 2

        # Đường đi player (trắng-xanh)
        if len(self.adv_player_path) > 1:
            pts_p = [(self.offset[0] + c * TILE_SIZE + TILE_SIZE // 2,
                      self.offset[1] + r * TILE_SIZE + TILE_SIZE // 2)
                     for r, c in self.adv_player_path]
            pygame.draw.lines(self.surface, (200, 255, 255), False, pts_p, 3)

        # Đường đi enemy (đỏ)
        if len(self.adv_enemy_path) > 1:
            pts_e = [(self.offset[0] + c * TILE_SIZE + TILE_SIZE // 2,
                      self.offset[1] + r * TILE_SIZE + TILE_SIZE // 2)
                     for r, c in self.adv_enemy_path]
            pygame.draw.lines(self.surface, (255, 80, 80), False, pts_e, 3)

        # Player
        pygame.draw.circle(self.surface, (255, 255, 255), (int(px), int(py)), TILE_SIZE // 3)
        # Enemy
        pygame.draw.circle(self.surface, (255, 50, 50), (int(ex), int(ey)), TILE_SIZE // 3)

        # Chữ P và E
        font = pygame.font.Font(None, 20)
        p_text = font.render("P", True, (0, 0, 0))
        e_text = font.render("E", True, (0, 0, 0))
        self.surface.blit(p_text, (px - 6, py - 8))
        self.surface.blit(e_text, (ex - 6, ey - 8))

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