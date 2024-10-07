from enum import Enum
from src.worlds import WorldData
from pyray import *
from src.shared import TempestColors, EventManager
from src.utils import Vec2
from src.entities import Flipper
import os, json
from importlib import import_module, resources


class Level:
    """
    Level class should handle:
    - Level states.
    - World drawing.
    - Enemies creations / deletions.
    """

    class States(Enum):
        LEVEL_BEGIN = 0
        LEVEL_COMPLETE = 1
        LEVEL_READY = 2
    

    def __init__(self, event_manager: EventManager):
        self.event_manager = (
            event_manager  # Common API to send/recibe data between objects.
        )
        self.event_manager.subscribe(EventManager.Topics.BLASTER_BORDER_UPDATE, self.blaster_border_update)
        self.enemies = []
        self.active_enemies = []

    def update(self):
        self._update_enemies()
    
    
    def blaster_border_update(self, data: dict):
        self.blaster_border = data["border_idx"]

    
    # TODO: Use pydantic models to parse jsons
    def load_level_data(self, level_number: int):
        """
        Load level data extracted from levels.json.
        """
        with resources.open_text('src.levels', 'levels.json') as f:
            data = json.load(f).get(str(level_number))
            
            world_data = data.get("world")
            worlds_module = import_module("src.worlds")
            self.world = getattr(worlds_module, world_data["name"])
            
            shared_module = import_module("src.shared")
            tempest_colors = getattr(shared_module, "TempestColors")
            self.level_color = getattr(tempest_colors, world_data["color"]).rgba()
            
            enemies_data = data.get("enemies")
            entities_module = import_module("src.entities")
            for enemy_name in enemies_data:
                for _ in range(enemies_data[enemy_name]["quantity"]):
                    enemy = getattr(entities_module, enemy_name)(
                        border_idx = 0,
                        world = self.world,
                        velocity = enemies_data[enemy_name]["velocity"],
                        event_manager = self.event_manager
                    )
                    self.enemies.append(enemy)


    def draw(self):
        self._draw_world()
        self._draw_enemies()

    def _draw_world(self):
        proyections = self.world.get_proyections()
        for i in range(16):
            draw_circle(int(self.world.x[i]), int(self.world.y[i]), 2, self.level_color)
            border_vec = Vector2(self.world.x[i], self.world.y[i])
            draw_circle_v(proyections[i], 1, self.level_color)
            draw_line_ex(border_vec, proyections[i], 2, self.level_color)
            if i > 0:
                current_vec = Vector2(self.world.x[i], self.world.y[i])
                previous_vec = Vector2(self.world.x[i - 1], self.world.y[i - 1])
                draw_line_ex(current_vec, previous_vec, 2, self.level_color)
                draw_line_ex(proyections[i], proyections[i - 1], 1, self.level_color)
        else:
            if self.world.is_loop:
                current_vec = Vector2(self.world.x[0], self.world.y[0])
                last_vec = Vector2(self.world.x[-1], self.world.y[-1])
                draw_line_ex(current_vec, last_vec, 2, self.level_color)
                draw_line_ex(proyections[0], proyections[-1], 1, self.level_color)

        # Change color of blaster current border section  -> /_x_\ <-
        border = Vec2(
            self.world.x[self.blaster_border], self.world.y[self.blaster_border]
        )
        # /__\* <- right border
        next_border = Vec2(
            self.world.x[self.blaster_border - 1], self.world.y[self.blaster_border - 1]
        )
        proyections = self.world.get_proyections()
        draw_line_ex(
            border,
            proyections[self.blaster_border],
            2,
            TempestColors.YELLOW_NEON.rgba(),
        )
        draw_line_ex(
            next_border,
            proyections[self.blaster_border - 1],
            2,
            TempestColors.YELLOW_NEON.rgba(),
        )

    def _draw_enemies(self):
        for enemy in self.active_enemies:
            enemy.draw()
    
    def _update_enemies(self):
        for enemy in self.active_enemies:
            enemy.update()

    def rand_enemy_spawn(self):
        if len(self.enemies):
            random_enemy_idx = get_random_value(0, len(self.enemies) - 1)
            enemy = self.enemies[random_enemy_idx]
            self.active_enemies.append(enemy)
            self.enemies.remove(enemy)
