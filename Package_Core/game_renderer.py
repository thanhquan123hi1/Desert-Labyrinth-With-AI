# Package_Core/game_renderer.py
import pygame, math, random
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
        self.effect_name = effect_name  # lưu loại môi trường
        self.player_group = pygame.sprite.GroupSingle(player)

        # --- Chuẩn hóa goals thành list ---
        if isinstance(goals, (tuple, list)) and isinstance(goals[0], int):
            self.goals = [goals]
        else:
            self.goals = list(goals)

        # --- Sprite đích ---
        self.goal_anim = SpriteSheetAnimation(
            image_path="Resources/Animation/goal.png",
            frame_width=32, frame_height=32,
            frame_count=8, fps=8, loop=True
        )

        # --- Quản lý hiệu ứng ---
        self.visited_age = {}
        self.path_phase = 0.0

    # =====================================================================
    def draw(self, dt, visible_visited, visible_path):
        """Vẽ toàn cảnh bản đồ, visited, path, player và đích."""
        self.map_model.update(dt)
        self.map_model.draw(self.surface)

        colors = self.get_theme_colors(self.effect_name)

        # --- Hiệu ứng visited ---
        if visible_visited:
            self.draw_cells_energy(visible_visited, base_color=colors["visited"])

        # --- Hiệu ứng path ---
        if visible_path:
            self.path_phase += dt * 4.0
            self.draw_cells_pathpulse(visible_path, self.path_phase, base_color=colors["path"])

        # --- Đích ---
        self.goal_anim.update(dt)
        for (r, c) in self.goals:
            pos = (
                self.offset[0] + c * TILE_SIZE + TILE_SIZE // 2,
                self.offset[1] + r * TILE_SIZE + TILE_SIZE // 2
            )
            self.draw_goal_glow(pos, colors["goal"])
            self.goal_anim.draw(self.surface, pos, scale=1.0)

        # --- Player ---
        self.player.update(dt, self.map_model.collision_matrix)
        self.player_group.draw(self.surface)

    # =====================================================================
    def draw_cells_energy(self, cells, base_color=(80, 200, 255)):
        """Hiệu ứng năng lượng lan tỏa ở visited"""
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

    def draw_cells_pathpulse(self, cells, phase, base_color=(0, 255, 255)):
        """Đường cyan có ánh sáng chạy"""
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

    # =====================================================================
    def draw_goal_glow(self, pos, color):
        """Đích: phát sáng năng lượng theo môi trường"""
        x, y = pos
        t = pygame.time.get_ticks() * 0.004
        glow_surface = pygame.Surface((TILE_SIZE * 6, TILE_SIZE * 6), pygame.SRCALPHA)
        center = (TILE_SIZE * 3, TILE_SIZE * 3)

        pulse = 0.6 + 0.4 * math.sin(t)
        r, g, b = color
        for radius, alpha in [(50, 40), (35, 80), (20, 140)]:
            pygame.draw.circle(glow_surface, (int(r*pulse), int(g*pulse), int(b*pulse), alpha), center, radius)
        rect = glow_surface.get_rect(center=(x, y))
        self.surface.blit(glow_surface, rect)

    # =====================================================================
    def get_theme_colors(self, effect_name):
        """Trả về bảng màu theo môi trường"""
        themes = {
            "baocat":  {"visited": (255, 140, 30),  "path": (255, 170, 60), "goal": (255, 210, 80)},
            "snow":    {"visited": (130, 190, 255), "path": (150, 220, 255), "goal": (255, 255, 255)},
            "leaves":  {"visited": (60, 170, 60),   "path": (80, 200, 80),  "goal": (180, 255, 180)},
            "rain":    {"visited": (40, 110, 220),  "path": (60, 140, 255), "goal": (200, 220, 255)},
            "fireflies":  {"visited": (255, 200, 70),  "path": (220, 200, 80), "goal": (255, 255, 180)},
        }
        return themes.get(effect_name, themes["baocat"])

    # =====================================================================
    def reset_effects(self):
        """Reset toàn bộ hiệu ứng (visited, path, pha sáng) khi bắt đầu chạy thuật toán mới"""
        self.visited_age.clear()
        self.path_phase = 0.0
