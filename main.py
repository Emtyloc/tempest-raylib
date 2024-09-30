from pyray import *
from raylib import ffi
from src.worlds import *
from src.level import Level
from src.utils import vector2_center_scale
from src.shared import TempestColors, SCREEN_CENTER, SCREEN_HEIGHT, SCREEN_WIDTH, TARGET_FPS, LEVEL
from src.entities import Blaster
import os


def draw_world(level_data: LevelData, color: TempestColors):

    PROYECTION_SCALE = 0.12 # Scale original level figure to make proyection figure
    for i in range(16):
        # Draw points around junctions
        draw_circle(int(level_data.x[i]), int(level_data.y[i]), 2, color.rgba())
        # Draw section lines between Border and scaled Proyection
        border_vec = Vector2(level_data.x[i],level_data.y[i])
        center_scaled = vector2_center_scale(border_vec, SCREEN_CENTER, PROYECTION_SCALE)
        proyection_vec = Vector2(center_scaled.x, center_scaled.y + level_data.y3d)
        
        # Draw point around proyection junctions 
        draw_circle(int(proyection_vec.x), int(proyection_vec.y), 1, color.rgba())

        draw_line_ex(border_vec, proyection_vec, 2, color.rgba())
        if i > 0:
            # Border lines
            current_vec = Vector2(level_data.x[i], level_data.y[i])
            previous_vec = Vector2(level_data.x[i-1], level_data.y[i-1])
            draw_line_ex(current_vec, previous_vec, 2, color.rgba())
            
            # Proyection lines
            current_scaled = vector2_center_scale(current_vec, SCREEN_CENTER, PROYECTION_SCALE)
            current_proyection = Vector2(current_scaled.x, current_scaled.y + level_data.y3d)
            
            previous_scaled = vector2_center_scale(previous_vec, SCREEN_CENTER, PROYECTION_SCALE)
            previous_proyection = Vector2(previous_scaled.x, previous_scaled.y + level_data.y3d)

            draw_line_ex(current_proyection, previous_proyection, 1, color.rgba())

    else:
        if level_data.is_loop:
            # Last border
            current_vec = Vector2(level_data.x[0],level_data.y[0])
            last_vec = Vector2(level_data.x[-1], level_data.y[-1])
            draw_line_ex(current_vec, last_vec, 2, color.value)

            # Last proyection border
            current_scale = vector2_center_scale(current_vec, SCREEN_CENTER, PROYECTION_SCALE)
            current_proyection = Vector2(current_scale.x, current_scale.y + level_data.y3d)

            last_scale = vector2_center_scale(last_vec, SCREEN_CENTER, PROYECTION_SCALE)
            last_proyection = Vector2(last_scale.x, last_scale.y + level_data.y3d)

            draw_line_ex(current_proyection, last_proyection, 1, color.value)


def main():
    
    init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Tempest Raylib")
    set_target_fps(TARGET_FPS)

    # CAMERA SETTINGS
   
    camera = Camera2D()
    camera.target = SCREEN_CENTER  # WHERE THE CAMARA IS LOCATED INSIDE THE GAME
    camera.offset = (
        SCREEN_CENTER  # WHERE THE CAMERA IMAGE IS DISPLAYED IN THE PLAYER SCREEN
    )
    camera.rotation = 0
    camera.zoom = 1.0

    world_idx = 0
    worlds = [circle_world, square_world, plus_world, peanut_world, cross_world, triangle_world, clover_world, vee_world, steps_world, u_shape_world, line_world, heart_world, star_world, w_shape_world, broken_v_world, infinity_world]
    
    # Its important to use os.path with dirname(__file__) to make files reachables from .exe/.bin builds.
    shader_path = os.path.join(os.path.dirname(__file__), "shaders/glsl330/bloom.fs")
    gloom_shader = load_shader("0", shader_path);

    set_shader_value(gloom_shader, get_shader_location(gloom_shader,"size"), Vector2(SCREEN_WIDTH, SCREEN_HEIGHT) , ShaderUniformDataType.SHADER_UNIFORM_VEC2)
    set_shader_value(gloom_shader, get_shader_location(gloom_shader,"samples"), ffi.new("float *", 11.0) , ShaderUniformDataType.SHADER_UNIFORM_FLOAT)
    set_shader_value(gloom_shader, get_shader_location(gloom_shader,"quality"), ffi.new("float *", 1.0) , ShaderUniformDataType.SHADER_UNIFORM_FLOAT)


    render_texture = load_render_texture(SCREEN_WIDTH, SCREEN_HEIGHT)

    blaster = Blaster()

    # Main game loop
    while not window_should_close():
        # LOOP SETTINGS BEFORE START THE RENDERING - BEGIN_DRAWING

        if is_key_pressed(KeyboardKey.KEY_D):
            if world_idx == len(worlds) - 1:
                world_idx = 0
            else:
                world_idx+=1
        elif is_key_pressed(KeyboardKey.KEY_A):
            if world_idx == 0:
                world_idx = len(worlds) - 1
            else:
                world_idx-=1
        
        LEVEL.world = worlds[world_idx]

        blaster.update()
        
        begin_drawing()

        begin_texture_mode(render_texture)
        clear_background(BLACK)
        # camera.rotation+=0.1
        begin_mode_2d(camera)
        # draw_circle(int(SCREEN_CENTER.x), int(SCREEN_CENTER.y), 1, GREEN)
        draw_world(LEVEL.world, TempestColors.BLUE_NEON)
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
