from enum import IntEnum, auto
from importlib import import_module, resources
import json

from src.levels import Level
from src.shared import EventManager, SCREEN_CENTER, TempestColors, SCREEN_WIDTH
from src.entities import Blaster
from src.sounds import SoundManager
from src.score import ScoreManager
from src.utils import Vec2
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
        self.current_level = 1
        self.max_level = 16  # Set maximum number of levels
        self.min_level = 1
        self.selected_level = 1  # Track the currently selected level

    def goto_level_selection(self):
        self.game_state = GameState.LEVEL_SELECTION

    def select_level(self, level_number: int):
        # Init level
        # TODO: improve handle game logics to avoid bugs as ghost entities, triggering events.

        self.event_manager.level_reset()

        self.level = Level(self.event_manager, self.sound_manager)
        self.level.load_level_data(level_number)

        self.score_manager = ScoreManager(self.event_manager)

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
                if is_key_pressed(KeyboardKey.KEY_RIGHT) and self.selected_level < self.max_level:
                    self.selected_level += 1
                    play_sound(self.sound_manager.get_sound("blaster_move"))
                elif is_key_pressed(KeyboardKey.KEY_LEFT) and self.selected_level > self.min_level:
                    self.selected_level -= 1
                    play_sound(self.sound_manager.get_sound("blaster_move"))
                elif is_key_pressed(KeyboardKey.KEY_ENTER):
                    self.current_level = self.selected_level
                    self.select_level(self.current_level)

            case GameState.PLAYING:
                self.blaster.update_frame()
                self.level.update_frame()
                if not self.blaster.alive:
                    self.game_state = GameState.LEVEL_SELECTION
                elif self.level.is_over():
                    self.current_level = min(self.current_level + 1, self.max_level)
                    self.select_level(self.current_level)

    def draw_start_screen(self):
        # Define font sizes and padding
        H1_SIZE_px = 40
        H2_SIZE_px = 20
        H3_SIZE_px = 15
        PAD_TOP_CENTER = 20

        # Draw the title
        title = "ATARI TEMPEST"
        x_pos = int(SCREEN_CENTER.x - measure_text(title, H1_SIZE_px) / 2)
        y_pos = int(SCREEN_CENTER.y - H1_SIZE_px)
        draw_text(title, x_pos, y_pos, H1_SIZE_px, TempestColors.PURPLE_NEON.rgba)

        # Draw blinking sub-title
        sub_title = "PRESS ENTER"
        pad_top = PAD_TOP_CENTER
        x_pos = int(SCREEN_CENTER.x - measure_text(sub_title, H2_SIZE_px) / 2)
        y_pos = int(SCREEN_CENTER.y - H2_SIZE_px + pad_top)
        draw_text(sub_title, x_pos, y_pos, H2_SIZE_px, TempestColors.TURQUOISE_NEON.rgba)

        # Draw controls title
        controls_title = "CONTROLS"
        pad_top = PAD_TOP_CENTER * 3
        x_pos = int(SCREEN_CENTER.x - measure_text(controls_title, H3_SIZE_px) / 2)
        y_pos = int(SCREEN_CENTER.y - H3_SIZE_px + pad_top)
        draw_text(controls_title, x_pos, y_pos, H3_SIZE_px, TempestColors.YELLOW_NEON.rgba)

        # Draw movement title
        movement_title = "MOVEMENT"
        pad_top = PAD_TOP_CENTER * 5
        x_pos = int(SCREEN_CENTER.x / 2 - measure_text(movement_title, H2_SIZE_px) / 2)
        y_pos = int(SCREEN_CENTER.y - H2_SIZE_px + pad_top)
        draw_text(movement_title, x_pos, y_pos, H2_SIZE_px, TempestColors.GREEN_NEON.rgba)

        # Draw shot title
        shot_title = "SHOT"
        pad_top = PAD_TOP_CENTER * 5
        x_pos = int(SCREEN_WIDTH - SCREEN_CENTER.x / 2 - measure_text(shot_title, H2_SIZE_px) / 2)
        y_pos = int(SCREEN_CENTER.y - H2_SIZE_px + pad_top)
        draw_text(shot_title, x_pos, y_pos, H2_SIZE_px, TempestColors.GREEN_NEON.rgba)

        # Draw left arrow
        left_arrow = "<-"
        pad_top = PAD_TOP_CENTER * 7
        x_pos = int(SCREEN_CENTER.x / 2 - SCREEN_CENTER.x / 8 - measure_text(left_arrow, H2_SIZE_px) / 2)
        y_pos = int(SCREEN_CENTER.y - H2_SIZE_px + pad_top)
        draw_text(left_arrow, x_pos, y_pos, H2_SIZE_px, TempestColors.RED_NEON.rgba)

        # Draw right arrow
        right_arrow = "->"
        x_pos = int(SCREEN_CENTER.x / 2 + SCREEN_CENTER.x / 8 - measure_text(right_arrow, H2_SIZE_px) / 2)
        draw_text(right_arrow, x_pos, y_pos, H2_SIZE_px, TempestColors.RED_NEON.rgba)

        # Draw shot key
        shot_key = "A"
        x_pos = int(SCREEN_WIDTH - SCREEN_CENTER.x / 2 - measure_text(shot_key, H2_SIZE_px) / 2)
        draw_text(shot_key, x_pos, y_pos, H2_SIZE_px, TempestColors.RED_NEON.rgba)



    def draw_level_selection(self):
        title = "SELECT LEVEL"
        draw_text(title, int(SCREEN_CENTER.x - measure_text(title, 40) / 2), int(SCREEN_CENTER.y - 100), 40, TempestColors.TURQUOISE_NEON.rgba)

        box_width = 80
        box_height = 120
        box_padding = 20
        border_size = 5

        num_levels = self.max_level - self.min_level + 1
        visible_levels = min(num_levels, 5)
        start_x = SCREEN_CENTER.x - (visible_levels * (box_width + box_padding)) // 2

        offset = (self.selected_level - (self.min_level + visible_levels // 2)) * (box_width + box_padding)
        start_x -= offset

        for level in range(self.min_level, self.max_level + 1):
            x_pos = start_x + (level - self.min_level) * (box_width + box_padding)
            y_pos = SCREEN_CENTER.y

            inner_color = TempestColors.BLACK_NEON.rgba
            if level == self.selected_level:
                outer_color = TempestColors.YELLOW_NEON.rgba
            else:
                outer_color = TempestColors.PURPLE_NEON.rgba

            # Draw the outer rectangle (border)
            draw_rectangle(int(x_pos - border_size), int(y_pos - border_size), int(box_width + border_size * 2), int(box_height + border_size * 2), outer_color)

            # Draw the inner rectangle
            draw_rectangle(int(x_pos), int(y_pos), int(box_width), int(box_height), inner_color)

            shape_preview_height = int(box_height * 0.7)
            self.draw_level_shape_preview(level, x_pos, y_pos, box_width, shape_preview_height)


            text_y_pos = y_pos + shape_preview_height + 5
            draw_text(str(level), int(x_pos + box_width / 2 - measure_text(str(level), 30) / 2), int(text_y_pos), 30, outer_color)

        left_arrow = "<-" if self.selected_level > self.min_level else ""
        right_arrow = "->" if self.selected_level < self.max_level else ""
        draw_text(left_arrow, int(SCREEN_CENTER.x - 200), int(SCREEN_CENTER.y + 140), 30, TempestColors.RED_NEON.rgba)
        draw_text(right_arrow, int(SCREEN_CENTER.x + 150), int(SCREEN_CENTER.y + 140), 30, TempestColors.RED_NEON.rgba)

        action = "PRESS ENTER TO SELECT"
        draw_text(action, int(SCREEN_CENTER.x - measure_text(action, 20) / 2), int(SCREEN_CENTER.y + 150), 20, TempestColors.TURQUOISE_NEON.rgba)


    def draw_frame(self):
        match self.game_state:
            case GameState.START_SCREEN:
                self.draw_start_screen()


            case GameState.LEVEL_SELECTION:
                self.draw_level_selection()

            case GameState.PLAYING:
                self.level.draw_frame()
                self.blaster.draw_frame()
                self.score_manager.draw_frame()
                self.draw_blaster_lives()

    def draw_blaster_lives(self):
        TOP_PADDING_px = 60

        LIVE_WIDTH_px = 30

        REFERENCE_x_px = int(SCREEN_CENTER.x / 6)
        
        for n in range(1, self.blaster.lives + 1):
            left_anchor_v = Vec2(REFERENCE_x_px * n, TOP_PADDING_px)
            right_anchor_v = Vec2(REFERENCE_x_px * n + LIVE_WIDTH_px, TOP_PADDING_px)
            height = 10
            tong_height = 5

            blaster_tip_v = left_anchor_v.lerp(right_anchor_v, 0.5)
            blaster_tip_v = Vec2(blaster_tip_v.x, blaster_tip_v.y + height)

            left_tong_v = left_anchor_v.lerp(right_anchor_v, 0.3)
            left_tong_v = Vec2(left_tong_v.x, left_tong_v.y - tong_height)
            
            right_tong_v = left_anchor_v.lerp(right_anchor_v, 0.7)
            right_tong_v = Vec2(right_tong_v.x, right_tong_v.y - tong_height)

            draw_line_ex(left_anchor_v, blaster_tip_v, 3, TempestColors.YELLOW_NEON.rgba)
            draw_line_ex(right_anchor_v, blaster_tip_v, 3, TempestColors.YELLOW_NEON.rgba)
            
            draw_line_ex(left_anchor_v, left_tong_v, 3, TempestColors.YELLOW_NEON.rgba)
            draw_line_ex(right_anchor_v, right_tong_v, 3, TempestColors.YELLOW_NEON.rgba)
    

    def draw_level_shape_preview(self, level, x_pos, y_pos, box_width, shape_preview_height):
        with resources.open_text('src.levels', 'levels.json') as f:
            data = json.load(f).get(str(level))

        world_data = data.get("world")
        worlds_module = import_module("src.worlds")
        world_shape = getattr(worlds_module, world_data["name"])

        shared_module = import_module("src.shared")
        tempest_colors = getattr(shared_module, "TempestColors")
        shape_color = getattr(tempest_colors, world_data["color"]).rgba

        is_loop = world_shape.is_loop

        max_shape_width = max([vec.x for vec in world_shape.borders]) - min([vec.x for vec in world_shape.borders])
        max_shape_height = max([vec.y for vec in world_shape.borders]) - min([vec.y for vec in world_shape.borders])

        if max_shape_width == 0:
            max_shape_width = 1
        if max_shape_height == 0:
            max_shape_height = 1


        # Scale to fit the shape within the box (both width and height)
        scale_x = (box_width * 0.8) / max_shape_width
        scale_y = (shape_preview_height * 0.8) / max_shape_height
        scale = min(scale_x, scale_y)

        # Center the shape within the preview area
        min_x = min([vec.x for vec in world_shape.borders])
        min_y = min([vec.y for vec in world_shape.borders])
        offset_x = x_pos + box_width // 2 - ((max_shape_width * scale) / 2)
        offset_y = y_pos + shape_preview_height // 2 - ((max_shape_height * scale) / 2)

        # Draw the level shape by connecting the vertices of the borders
        for i in range(len(world_shape.borders) - (0 if is_loop else 1)):
            start = world_shape.borders[i]
            end = world_shape.borders[(i + 1) % len(world_shape.borders)] if is_loop else world_shape.borders[i + 1]

            draw_line(
                int(offset_x + (start.x - min_x) * scale),
                int(offset_y + (start.y - min_y) * scale),
                int(offset_x + (end.x - min_x) * scale),
                int(offset_y + (end.y - min_y) * scale),
                shape_color
            )
