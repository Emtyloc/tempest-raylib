from src.worlds import WorldData
from .enemy import Enemy
from src.utils import Vec2
from src.shared import EventManager, TempestColors, SCREEN_CENTER
from src.sounds import SoundManager
from pyray import * 
import math
import random

class Fuseball(Enemy):
    class State:
        MOVING_TO_BORDER = 0
        MOVING_ALONG_BORDER = 1

    def __init__(self, border_idx: int, world: WorldData, velocity: float, event_manager: EventManager, sound_manager: SoundManager):
        super().__init__(border_idx, world, velocity, event_manager, sound_manager)
        
        self.position = Vec2(SCREEN_CENTER.x, SCREEN_CENTER.y)
        self.blaster_position = None
        
        self.target_position = Vec2(world.proyections[border_idx].x, world.proyections[border_idx].y)
        
        self.final_position = Vec2(world.borders[border_idx].x, world.borders[border_idx].y)
        
        self.state = self.State.MOVING_TO_BORDER
        self.velocity = velocity
        self.color = TempestColors.PURPLE_NEON.rgba
        self.alive = True
        self.active = False

        self.border_idx = border_idx
        self.direction = 1 if random.random() < 0.5 else -1
        self.next_border_idx = (self.border_idx + self.direction) % len(self.world.borders)

        self.event_manager.subscribe(EventManager.Topics.BLASTER_BORDER_UPDATE, self.blaster_border_update)
        self.event_manager.subscribe(EventManager.Topics.BLASTER_BULLET_UPDATE, self.blaster_bullet_update)

    def update_frame(self):
        """ Actualiza la posición y el estado del Fuseball """
        if not self.active:
            return

        if self.state == self.State.MOVING_TO_BORDER:
            self.move_to_border()
        elif self.state == self.State.MOVING_ALONG_BORDER:
            self.move_along_border()

        if self.collides_with_player():
            self.handle_collision_with_player()

    def move_to_border(self):
        """ Mueve el Fuseball hacia el borde siguiendo las proyecciones """
        direction_vec = Vec2(self.target_position.x - self.position.x, self.target_position.y - self.position.y)
        distance = direction_vec.length()

        if distance < self.velocity:
            self.position = self.target_position
            self.target_position = self.final_position

            if self.position == self.final_position:
                self.state = self.State.MOVING_ALONG_BORDER
                self.velocity /= 2
        else:
            direction_vec.normalize()
            self.position.x += direction_vec.x * self.velocity
            self.position.y += direction_vec.y * self.velocity

    def move_along_border(self):
        """ Mueve el Fuseball a lo largo del borde de manera continua """
        current_border = Vec2(self.world.borders[self.border_idx].x, self.world.borders[self.border_idx].y)
        next_border = Vec2(self.world.borders[self.next_border_idx].x, self.world.borders[self.next_border_idx].y)
        
        direction_vec = Vec2(next_border.x - current_border.x, next_border.y - current_border.y)
        distance = direction_vec.length()

        if distance < self.velocity:
            self.position = Vec2(next_border.x, next_border.y)
            self.border_idx = self.next_border_idx
            self.direction = 1 if random.random() < 0.5 else -1
            self.next_border_idx = (self.border_idx + self.direction) % len(self.world.borders)
        else:
            direction_vec.normalize()
            self.position.x += direction_vec.x * self.velocity
            self.position.y += direction_vec.y * self.velocity

            if abs(self.position.x - next_border.x) < 0.1 and abs(self.position.y - next_border.y) < 0.1:
                self.position = Vec2(next_border.x, next_border.y)
                self.border_idx = self.next_border_idx
                self.next_border_idx = (self.border_idx + self.direction) % len(self.world.borders)

    def blaster_border_update(self, data: dict):
        """ Actualiza la posición del jugador cuando cambia de borde """
        blaster_border_idx = data["border_idx"]
        self.blaster_position = self.world.borders[blaster_border_idx]  # Actualiza la posición del jugador según su borde actual

    def collides_with_player(self):
        """ Verifica si hay colisión con el jugador usando la posición actualizada del evento """
        if self.blaster_position:
            return check_collision_circles(self.position, 10, self.blaster_position, 10)  # Verifica si las posiciones están lo suficientemente cerca
        return False

    def handle_collision_with_player(self):
        """ Lógica cuando colisiona con el jugador """
        print("Jugador impactado por una Fuseball!")
        self.event_manager.notify(EventManager.Topics.BLASTER_DEAD, {})
        self.alive = False

    def blaster_bullet_update(self, data: dict):
        """ Maneja colisiones con disparos del jugador """
        bullet = data["bullet"]
        if check_collision_circles(bullet.position, bullet.radio, self.position, 10):
            print("Fuseball destruida por un blaster!")
            self.alive = False
            self.active = False
            self.event_manager.notify(EventManager.Topics.BLASTER_BULLET_COLLIDE, {"bullet": bullet})
            self.event_manager.unsubscribe(EventManager.Topics.BLASTER_BULLET_UPDATE, self.blaster_bullet_update)

    def draw_frame(self):
        """ Dibuja el Fuseball en la pantalla """
        if self.active:
            draw_circle(int(self.position.x), int(self.position.y), 10, self.color)

    def destroy(self):
        """ Desuscribirse de eventos cuando la Fuseball es destruida """
        self.event_manager.unsubscribe(EventManager.Topics.BLASTER_BULLET_UPDATE, self.blaster_bullet_update)
