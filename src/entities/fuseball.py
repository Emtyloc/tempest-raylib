from src.worlds import WorldData
from .enemy import Enemy
from src.utils import Vec2
from src.shared import EventManager, TempestColors, SCREEN_CENTER
from src.sounds import SoundManager
from pyray import * 
from pyray import Color
import math
import random


class Fuseball(Enemy):
    class State:
        MOVING_TO_BORDER = 0
        MOVING_ALONG_BORDER = 1

    def __init__(self, border_idx: int, world: WorldData, velocity: float, event_manager: EventManager, sound_manager: SoundManager):
        super().__init__(border_idx, world, velocity, event_manager, sound_manager)
        self.position = Vec2(SCREEN_CENTER.x, SCREEN_CENTER.y)  # Posición inicial en el centro
        self.target_position = world.borders[border_idx]  # Posición de destino (el borde)
        self.state = self.State.MOVING_TO_BORDER  # Estado inicial: moviéndose hacia el borde
        self.velocity = velocity * 2  # Velocidad rápida inicial
        self.direction = 1  # Dirección de movimiento
        self.radius = world.borders[border_idx].distance(SCREEN_CENTER)  # Distancia al borde
        self.color = TempestColors.PURPLE_NEON.rgba # Color del Fuseball
        self.alive = True  # Estado de vida del Fuseball
        self.active = False  # Si el Fuseball está activo o no

    def update_frame(self):
        """ Actualiza la posición y el estado del Fuseball """
        if not self.active:  # Si el Fuseball no está activo, no se mueve
            return

        if self.state == self.State.MOVING_TO_BORDER:
            self.move_to_border()
        elif self.state == self.State.MOVING_ALONG_BORDER:
            self.move_along_border()

        # Verifica colisiones con el jugador o con otros elementos
        if self.collides_with_player():
            self.handle_collision_with_player()

    def move_to_border(self):
        """ Mueve el Fuseball hacia el borde a gran velocidad """
        direction_vec = Vec2(self.target_position.x - self.position.x, self.target_position.y - self.position.y)
        distance = direction_vec.length()

        if distance < self.velocity:  # Si está cerca del borde, cambia el estado
            self.position = self.target_position
            self.state = self.State.MOVING_ALONG_BORDER
            self.velocity /= 2  # Reduce la velocidad al llegar al borde
        else:
            direction_vec.normalize()
            self.position.x += direction_vec.x * self.velocity
            self.position.y += direction_vec.y * self.velocity

    def move_along_border(self):
        """ Mueve el Fuseball entre los segmentos del borde a menor velocidad """
        self.angle += self.velocity * self.direction
        self.position.x = self.radius * math.cos(self.angle) + SCREEN_CENTER.x
        self.position.y = self.radius * math.sin(self.angle) + SCREEN_CENTER.y

        # Cambio aleatorio de dirección entre segmentos del borde
        if random.random() < 0.01:  # Cambiar la dirección aleatoriamente
            self.direction *= -1

    def draw_frame(self):
        """ Dibuja el Fuseball en la pantalla """
        if self.active:  # Solo dibuja si está activo
            draw_circle(int(self.position.x), int(self.position.y), 10, self.color)

    def collides_with_player(self):
        """ Lógica de colisión con el jugador """
        # Aquí puedes agregar la lógica para verificar si colisiona con el jugador
        return False

    def handle_collision_with_player(self):
        """ Lógica cuando colisiona con el jugador """
        self.alive = False
        # Aquí puedes agregar lógica para eliminar o desactivar el Fuseball cuando colisione

    def blaster_bullet_update(self, data: dict):
        """ Evento que maneja la colisión con disparos """
        # Las Fuseballs son invulnerables a los disparos
        pass

    def blaster_border_update(self, data: dict):
        """ Evento que maneja la actualización del borde del blaster """
        pass
