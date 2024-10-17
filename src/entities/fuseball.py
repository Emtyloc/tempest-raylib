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
        
        # Iniciar en el centro geométrico de la figura
        self.position = Vec2(SCREEN_CENTER.x, SCREEN_CENTER.y)
        
        # Proyección inicial hacia la que se moverá
        self.target_position = Vec2(world.proyections[border_idx].x, world.proyections[border_idx].y)
        
        # Posición final en el borde del nivel
        self.final_position = Vec2(world.borders[border_idx].x, world.borders[border_idx].y)
        
        self.state = self.State.MOVING_TO_BORDER  # Estado inicial: moviéndose hacia el borde
        self.velocity = velocity # Velocidad inicial
        self.color = TempestColors.PURPLE_NEON.rgba
        self.alive = True
        self.active = False  # Si el Fuseball está activo o no

        # Para el movimiento a lo largo del borde
        self.border_idx = border_idx
        self.direction = 1 if random.random() < 0.5 else -1  # Dirección aleatoria: 1 (siguiente) o -1 (anterior)
        self.next_border_idx = (self.border_idx + self.direction) % len(self.world.borders)

    def update_frame(self):
        """ Actualiza la posición y el estado del Fuseball """
        if not self.active:
            return

        if self.state == self.State.MOVING_TO_BORDER:
            self.move_to_border()  # Mover hacia el borde
        elif self.state == self.State.MOVING_ALONG_BORDER:
            self.move_along_border()  # Mover a lo largo del borde

        # Verifica colisiones con el jugador o con otros elementos
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
                self.velocity /= 2  # Reduce la velocidad para moverse por el borde
        else:
            direction_vec.normalize()
            self.position.x += direction_vec.x * self.velocity
            self.position.y += direction_vec.y * self.velocity

    def move_along_border(self):
        """ Mueve el Fuseball a lo largo del borde de manera continua en una dirección aleatoria """
        current_border = Vec2(self.world.borders[self.border_idx].x, self.world.borders[self.border_idx].y)
        next_border = Vec2(self.world.borders[self.next_border_idx].x, self.world.borders[self.next_border_idx].y)
        
        # Vector de dirección entre los dos bordes
        direction_vec = Vec2(next_border.x - current_border.x, next_border.y - current_border.y)
        distance = direction_vec.length()
        
        print(f"distance: {distance}, current: {current_border}, next: {next_border}")
        
        # Si la distancia al siguiente borde es menor que la velocidad, ajusta la posición
        if distance < self.velocity:
            # Mueve la Fuseball al borde exacto sin sobrepasarlo
            self.position = Vec2(next_border.x, next_border.y)
            
            # Actualiza los índices para que se mueva al siguiente o anterior borde
            self.border_idx = self.next_border_idx
            self.direction = 1 if random.random() < 0.5 else -1  # Cambia aleatoriamente la dirección en cada borde
            self.next_border_idx = (self.border_idx + self.direction) % len(self.world.borders)
        
        else:
            # Mueve la Fuseball gradualmente hacia el siguiente borde
            direction_vec.normalize()
            self.position.x += direction_vec.x * self.velocity
            self.position.y += direction_vec.y * self.velocity

            # Verificación adicional para evitar quedarse en el mismo borde indefinidamente
            if abs(self.position.x - next_border.x) < 0.1 and abs(self.position.y - next_border.y) < 0.1:
                self.position = Vec2(next_border.x, next_border.y)
                self.border_idx = self.next_border_idx
                self.next_border_idx = (self.border_idx + self.direction) % len(self.world.borders)

    def draw_frame(self):
        """ Dibuja el Fuseball en la pantalla """
        if self.active:
            draw_circle(int(self.position.x), int(self.position.y), 10, self.color)

    def collides_with_player(self):
        """ Lógica de colisión con el jugador """
        return False

    def handle_collision_with_player(self):
        """ Lógica cuando colisiona con el jugador """
        self.alive = False

    def blaster_bullet_update(self, data: dict):
        """ Evento que maneja la colisión con disparos """
        pass

    def blaster_border_update(self, data: dict):
        """ Evento que maneja la actualización del borde del blaster """
        pass
