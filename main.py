from pyray import *
from raylib import ffi
from src.shared import TempestColors, SCREEN_CENTER, SCREEN_HEIGHT, SCREEN_WIDTH, TARGET_FPS, EventManager
from src.entities import Blaster, Level
from enum import IntEnum
import json
import os


def init_gloom_shader() -> Shader:
    # Its important to use os.path with dirname(__file__) to make files reachables from .exe/.bin builds.
    shader_path = os.path.join(os.path.dirname(__file__), "shaders/glsl330/bloom.fs")
    gloom_shader = load_shader("0", shader_path);
    set_shader_value(gloom_shader, get_shader_location(gloom_shader,"size"), Vector2(SCREEN_WIDTH, SCREEN_HEIGHT) , ShaderUniformDataType.SHADER_UNIFORM_VEC2)
    set_shader_value(gloom_shader, get_shader_location(gloom_shader,"samples"), ffi.new("float *", 11.0) , ShaderUniformDataType.SHADER_UNIFORM_FLOAT)
    set_shader_value(gloom_shader, get_shader_location(gloom_shader,"quality"), ffi.new("float *", 1.0) , ShaderUniformDataType.SHADER_UNIFORM_FLOAT)
    return gloom_shader

icon = load_image(os.path.join(os.path.dirname(__file__), "icon.ico"))
def setup_window():
    init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Tempest Raylib")
    set_window_icon(icon)
    set_target_fps(TARGET_FPS)

def init_2d_camera() -> Camera2D:
    camera = Camera2D()
    camera.target = SCREEN_CENTER  # WHERE THE CAMARA IS LOCATED INSIDE THE GAME
    camera.offset = (
        SCREEN_CENTER  # WHERE THE CAMERA IMAGE IS DISPLAYED IN THE PLAYER SCREEN
    )
    camera.rotation = 0
    camera.zoom = 1.0
    return camera

def main():
    
    # Engine setup
    setup_window()
    camera = init_2d_camera()
    gloom_shader = init_gloom_shader()
    render_texture = load_render_texture(SCREEN_WIDTH, SCREEN_HEIGHT)

    event_manager = EventManager()
    level = Level(event_manager)
    level.load_level_data(level_number = 1)
    blaster = Blaster(level.world, event_manager)
    

    # Main game loop
    while not window_should_close():

        if is_key_pressed(KeyboardKey.KEY_ENTER):
            level.rand_enemy_spawn()

        # Update game
        
        level.update()
        blaster.update()
        
        begin_drawing()

        begin_texture_mode(render_texture)
        
        clear_background(BLACK)
        begin_mode_2d(camera)
        
        # Draw game
        level.draw()
        blaster.draw()

        end_mode_2d()
        end_texture_mode()

        begin_shader_mode(gloom_shader) 
        draw_texture_rec(render_texture.texture, Rectangle(0,0, render_texture.texture.width, -render_texture.texture.height),Vector2(0,0), WHITE)
        end_shader_mode()

        draw_fps(0, 0)
        end_drawing()

    unload_shader(gloom_shader)
    unload_render_texture(render_texture)
    unload_image(icon)
    close_window()


if __name__ == "__main__":
    main()
