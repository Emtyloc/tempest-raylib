from enum import IntEnum, auto
from src.levels import Level
from src.shared import EventManager, SCREEN_CENTER, TempestColors, SCREEN_WIDTH
from src.entities import Blaster
from src.sounds import SoundManager
from src.score import ScoreManager
from pyray import *

class GameState(IntEnum):
    START_SCREEN = auto()
    LEVEL_SELECTION = auto()
    PLAYING = auto()

class Game:

    def __init__(self, sound_manager: SoundManager) -> None:
        self.sound_manager = sound_manager
        self.game_state = GameState.START_SCREEN
        self.event_manager = EventManager()
        self.score_manager = ScoreManager(self.event_manager)
        self.current_level = 1

    def goto_level_selection(self):
        self.game_state = GameState.LEVEL_SELECTION
    
    def select_level(self, level_number: int):
        # Init level
        # TODO: improve handle game logics to avoid bugs as ghost entities, triggering events.
        
        self.event_manager.level_reset()
        
        self.level = Level(self.event_manager, self.sound_manager)
        self.level.load_level_data(level_number)
        
        # Init Player
        self.blaster = Blaster(self.level.world, self.event_manager, self.sound_manager)

        self.game_state = GameState.PLAYING


    def update_frame(self):
        
        match self.game_state:
            case GameState.START_SCREEN:
                if is_key_pressed(KeyboardKey.KEY_ENTER):
                    self.goto_level_selection()
                #TODO: start screen animations

            case GameState.LEVEL_SELECTION:
                if is_key_pressed(KeyboardKey.KEY_RIGHT):
                    pass
                elif is_key_pressed(KeyboardKey.KEY_LEFT):
                    pass
                elif is_key_pressed(KeyboardKey.KEY_ENTER):
                    self.select_level(self.current_level)

            case GameState.PLAYING:
                self.blaster.update_frame()
                self.level.update_frame()
                if not self.blaster.alive:
                    self.game_state = GameState.LEVEL_SELECTION
                elif self.level.is_over():
                    # TODO: check level don't pass 16
                    self.current_level += 1
                    self.select_level(self.current_level)
    
    def draw_frame(self):
        match self.game_state:
            case GameState.START_SCREEN:
                H1_SIZE_px = 40
                H2_SIZE_px = 20
                H3_SIZE_px = 15
                PAD_TOP_CENTER = 20

                title = "ATARI TEMPEST"
                x_pos = int(SCREEN_CENTER.x - measure_text(title, H1_SIZE_px) / 2)
                y_pos = int(SCREEN_CENTER.y - H1_SIZE_px)
                draw_text(title, x_pos, y_pos, H1_SIZE_px, TempestColors.PURPLE_NEON.rgba)
                
                # TODO: Blinking text
                sub_title = "PRESS ENTER"
                pad_top = PAD_TOP_CENTER
                x_pos = int(SCREEN_CENTER.x - measure_text(sub_title, 20) / 2)
                y_pos = int(SCREEN_CENTER.y - H2_SIZE_px + pad_top)
                draw_text(sub_title, x_pos, y_pos, H2_SIZE_px, TempestColors.TURQUOISE_NEON.rgba)
                
                controls_title = "CONTROLS"
                pad_top = PAD_TOP_CENTER * 3
                x_pos = int(SCREEN_CENTER.x - measure_text(controls_title, H3_SIZE_px) / 2)
                y_pos = int(SCREEN_CENTER.y - H3_SIZE_px + pad_top)
                draw_text(controls_title, x_pos, y_pos, H3_SIZE_px, TempestColors.YELLOW_NEON.rgba)

                movement_title = "MOVEMENT"
                pad_top = PAD_TOP_CENTER * 5
                x_pos = int(SCREEN_CENTER.x / 2 - measure_text(movement_title, H2_SIZE_px) / 2)
                y_pos = int(SCREEN_CENTER.y - H2_SIZE_px + pad_top)
                draw_text(movement_title, x_pos, y_pos, H2_SIZE_px, TempestColors.GREEN_NEON.rgba)

                shot_title = "SHOT"
                pad_top = PAD_TOP_CENTER * 5
                x_pos = int(SCREEN_WIDTH - SCREEN_CENTER.x / 2 - measure_text(shot_title, H2_SIZE_px) / 2)
                y_pos = int(SCREEN_CENTER.y - H2_SIZE_px + pad_top)
                draw_text(shot_title, x_pos, y_pos, H2_SIZE_px, TempestColors.GREEN_NEON.rgba)
                
                left_arrow = "<-"
                pad_top = PAD_TOP_CENTER * 7
                x_pos = int(SCREEN_CENTER.x / 2 - SCREEN_CENTER.x / 8 - measure_text(left_arrow, H2_SIZE_px) / 2)
                y_pos = int(SCREEN_CENTER.y - H2_SIZE_px + pad_top)
                draw_text(left_arrow, x_pos, y_pos, H2_SIZE_px, TempestColors.RED_NEON.rgba)
                
                right_arrow = "->"
                pad_top = PAD_TOP_CENTER * 7
                x_pos = int(SCREEN_CENTER.x / 2 + SCREEN_CENTER.x / 8 - measure_text(right_arrow, H2_SIZE_px) / 2)
                y_pos = int(SCREEN_CENTER.y - H2_SIZE_px + pad_top)
                draw_text(right_arrow, x_pos, y_pos, H2_SIZE_px, TempestColors.RED_NEON.rgba)
                
                shot_key = "A"
                pad_top = PAD_TOP_CENTER * 7
                x_pos = int(SCREEN_WIDTH - SCREEN_CENTER.x / 2 - measure_text(shot_key, H2_SIZE_px) / 2)
                y_pos = int(SCREEN_CENTER.y - H2_SIZE_px + pad_top)
                draw_text(shot_key, x_pos, y_pos, H2_SIZE_px, TempestColors.RED_NEON.rgba)


            case GameState.LEVEL_SELECTION:
                title = "SELECT LEVEL"
                draw_text(title, int(SCREEN_CENTER.x - measure_text(title, 40) / 2), int(SCREEN_CENTER.y - 40), 40, TempestColors.TURQUOISE_NEON.rgba)
            case GameState.PLAYING:
                self.level.draw_frame()
                self.blaster.draw_frame()
                self.score_manager.draw_frame()

