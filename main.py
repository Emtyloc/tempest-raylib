from pyray import *
from raylib import ffi
from src.worlds import *
from src.shared import TempestColors, SCREEN_CENTER, SCREEN_HEIGHT, SCREEN_WIDTH, TARGET_FPS
from src.entities import Blaster
from src.level import LEVEL
import os


def init_gloom_shader() -> Shader:
    # Its important to use os.path with dirname(__file__) to make files reachables from .exe/.bin builds.
    shader_path = os.path.join(os.path.dirname(__file__), "shaders/glsl330/bloom.fs")
    gloom_shader = load_shader("0", shader_path);
    set_shader_value(gloom_shader, get_shader_location(gloom_shader,"size"), Vector2(SCREEN_WIDTH, SCREEN_HEIGHT) , ShaderUniformDataType.SHADER_UNIFORM_VEC2)
    set_shader_value(gloom_shader, get_shader_location(gloom_shader,"samples"), ffi.new("float *", 11.0) , ShaderUniformDataType.SHADER_UNIFORM_FLOAT)
    set_shader_value(gloom_shader, get_shader_location(gloom_shader,"quality"), ffi.new("float *", 1.0) , ShaderUniformDataType.SHADER_UNIFORM_FLOAT)
    return gloom_shader

def setup_window():
    init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Tempest Raylib")
    set_target_fps(TARGET_FPS)

def init_2d_camera() -> Camera2D:
    camera = Camera2D()
    camera.target = SCREEN_CENTER.vector2  # WHERE THE CAMARA IS LOCATED INSIDE THE GAME
    camera.offset = (
        SCREEN_CENTER.vector2  # WHERE THE CAMERA IMAGE IS DISPLAYED IN THE PLAYER SCREEN
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
    
    world_idx = 0
    worlds = [circle_world, square_world, plus_world, peanut_world, cross_world, triangle_world, clover_world, vee_world, steps_world, u_shape_world, line_world, heart_world, star_world, w_shape_world, broken_v_world, infinity_world]

    LEVEL.world = worlds[world_idx]
    blaster = Blaster()
    # Main game loop
    while not window_should_close():
        # LOOP SETTINGS BEFORE START THE RENDERING - BEGIN_DRAWING

        if is_key_pressed(KeyboardKey.KEY_D):
            if world_idx == len(worlds) - 1:
                world_idx = 0
            else:
                world_idx+=1
            LEVEL.world = worlds[world_idx]
            blaster.border_idx = LEVEL.world.start_idx
            blaster.position = blaster.Position.CENTER
        elif is_key_pressed(KeyboardKey.KEY_A):
            if world_idx == 0:
                world_idx = len(worlds) - 1
            else:
                world_idx-=1
            LEVEL.world = worlds[world_idx]
            blaster.border_idx = LEVEL.world.start_idx
            blaster.position = blaster.Position.CENTER
                

        blaster.update()
        
        begin_drawing()

        begin_texture_mode(render_texture)
        
        clear_background(BLACK)
        begin_mode_2d(camera)
        
        LEVEL.draw()
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
    close_window()


if __name__ == "__main__":
    main()
