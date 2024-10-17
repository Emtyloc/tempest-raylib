from enum import Enum
from src.worlds import WorldData
from pyray import *
from src.shared import TempestColors, EventManager
from src.utils import Vec2
from src.entities import Flipper
from src.sounds import SoundManager
import os, json
from importlib import import_module, resources


class Level:

    class States(Enum):
        LEVEL_BEGIN = 0
        LEVEL_COMPLETE = 1
        LEVEL_READY = 2
    

    def __init__(self, event_manager: EventManager, sound_manager: SoundManager):
        self.event_manager = (
            event_manager  # Common API to send/recibe data between objects.
        )
        self.sound_manager = sound_manager
        self.event_manager.subscribe(EventManager.Topics.BLASTER_BORDER_UPDATE, self.blaster_border_update)
        self.sleep_enemies = []
        self.active_enemies = []
        self.time_last_spawn = 1

    def update_frame(self):
        self._spawn_enemy()
        self._update_enemies()
    
    def _spawn_enemy(self):
        self.time_last_spawn += get_frame_time()
        if self.time_last_spawn >= self.spawn_time:
            if not self.sleep_enemies: return
            random_enemy = self.sleep_enemies[get_random_value(0, len(self.sleep_enemies) - 1)]
            random_enemy.active = True
            self.active_enemies.append(random_enemy)
            self.sleep_enemies.remove(random_enemy)
            self.time_last_spawn -= self.spawn_time
    
    def blaster_border_update(self, data: dict):
        self.blaster_border = data["border_idx"]
    
    
    def enemies_factory(self, enemies_data: dict):
        entities_module = import_module("src.entities")
        for enemy_name in enemies_data:
            for _ in range(enemies_data[enemy_name]["quantity"]):
                # Common enemy class atributes
                velocity = enemies_data[enemy_name]["velocity"]
                match enemy_name:
                    case "Flipper":
                        if self.world.is_loop:
                            start_idx = get_random_value(0, 15)
                        else:
                            start_idx = get_random_value(1, 15)
                        enemy = getattr(entities_module, enemy_name)(
                            border_idx = start_idx,
                            world = self.world,
                            velocity = velocity,
                            rotates = enemies_data[enemy_name]["rotates"],
                            event_manager = self.event_manager,
                            sound_manager = self.sound_manager
                        )
                        self.sleep_enemies.append(enemy)
                    case "Fuseball":
                        # Generar un índice aleatorio para los vértices del borde
                        start_idx = get_random_value(0, len(self.world.borders) - 1)
                        # Crear una instancia del Fuseball con posiciones aleatorias
                        enemy = getattr(entities_module, enemy_name)(
                            border_idx=start_idx,
                            world=self.world,
                            velocity=velocity,
                            event_manager=self.event_manager,
                            sound_manager=self.sound_manager,
                        )
                        self.sleep_enemies.append(enemy)
                    case _:
                        raise Exception(f"You need to implement the switch case for {enemy_name} to be constructed.")


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
            self.level_color = getattr(tempest_colors, world_data["color"]).rgba
            
            enemies_data = data.get("enemies")
            self.enemies_factory(enemies_data)
            
            self.spawn_time = data["spawn_time"]


    def draw_frame(self):
        self._draw_world()
        self._draw_enemies()

    def _draw_world(self):
        proyections = self.world.proyections
        for i in range(16):
            draw_circle_v(self.world.borders[i], 2, self.level_color)
            draw_circle_v(proyections[i], 1, self.level_color)
            draw_line_ex(self.world.borders[i], proyections[i], 2, self.level_color)
            if i > 0:
                current_vec = self.world.borders[i]
                previous_vec = self.world.borders[i - 1]
                draw_line_ex(current_vec, previous_vec, 2, self.level_color)
                draw_line_ex(proyections[i], proyections[i - 1], 1, self.level_color)
        else:
            if self.world.is_loop:
                current_vec = self.world.borders[0]
                last_vec = self.world.borders[-1]
                draw_line_ex(current_vec, last_vec, 2, self.level_color)
                draw_line_ex(proyections[0], proyections[-1], 1, self.level_color)

        # Change color of blaster current border section  -> /_x_\ <-
        border = self.world.borders[self.blaster_border]
        # /__\* <- right border
        next_border = self.world.borders[self.blaster_border - 1]
        proyections = self.world.proyections
        draw_line_ex(
            border,
            proyections[self.blaster_border],
            2,
            TempestColors.YELLOW_NEON.rgba,
        )
        draw_line_ex(
            next_border,
            proyections[self.blaster_border - 1],
            2,
            TempestColors.YELLOW_NEON.rgba,
        )

    def _draw_enemies(self):
        for enemy in self.active_enemies:
            enemy.draw_frame()
    
    def _update_enemies(self):
        for enemy in self.active_enemies[:]:
            if not enemy.alive:
                self.active_enemies.remove(enemy)

        for enemy in self.active_enemies:
            enemy.update_frame()

    def is_over(self):
        border_flippers = 0
        for enemy in self.active_enemies:
            if isinstance(enemy, Flipper) and enemy.position != enemy.Position.UPRIGHT:
                border_flippers += 1
        return (border_flippers == len(self.active_enemies) and not self.sleep_enemies)
