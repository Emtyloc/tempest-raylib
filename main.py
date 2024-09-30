from pyray import *
from raylib import ffi
from worlds import *
from enum import Enum


#SETTINGS
SCREEN_WIDTH: int = 600
SCREEN_HEIGHT: int = 800
TARGET_FPS = 60
SCREEN_CENTER = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

class TempestColors(Enum):
    BLUE_NEON = Color(31, 81, 255, 255)
    RED_NEON = Color(255, 49, 49, 255)
    GREEN_NEON = Color(15, 255, 80, 255)
    YELLOW_NEON = Color(223, 255, 0, 255)
    TURQUOISE_NEON = Color(64, 224, 208, 255)
    PURPLE_NEON = Color(191, 64, 191, 255)
    WHITE_NEON = RAYWHITE


def draw_world(level_data: LevelData, color: TempestColors):

    PROYECTION_SCALE = 0.12 # Scale original level figure to make proyection figure
    for i in range(16):
        # Draw points around junctions
        draw_circle(int(level_data.x[i]), int(level_data.y[i]), 2, color.value)
        # Draw section lines between Border and scaled Proyection
        border_vec = Vector2(level_data.x[i],level_data.y[i])
        center_scaled = vector2_center_scale(border_vec, SCREEN_CENTER, PROYECTION_SCALE)
        proyection_vec = Vector2(center_scaled.x, center_scaled.y + level_data.y3d)
        
        # Draw point around proyection junctions 
        draw_circle(int(proyection_vec.x), int(proyection_vec.y), 1, color.value)

        draw_line_ex(border_vec, proyection_vec, 2, color.value)
        if i > 0:
            # Border lines
            current_vec = Vector2(level_data.x[i], level_data.y[i])
            previous_vec = Vector2(level_data.x[i-1], level_data.y[i-1])
            draw_line_ex(current_vec, previous_vec, 2, color.value)
            
            # Proyection lines
            current_scaled = vector2_center_scale(current_vec, SCREEN_CENTER, PROYECTION_SCALE)
            current_proyection = Vector2(current_scaled.x, current_scaled.y + level_data.y3d)
            
            previous_scaled = vector2_center_scale(previous_vec, SCREEN_CENTER, PROYECTION_SCALE)
            previous_proyection = Vector2(previous_scaled.x, previous_scaled.y + level_data.y3d)

            draw_line_ex(current_proyection, previous_proyection, 1, color.value)

    else:
        if not level_data.open_state:
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


def vector2_center_scale(vector: Vector2, center: Vector2, scale_factor: float) -> Vector2:
    """
    Scale vector using center reference(vector) by scale factor.
    """
    offset_vector = vector2_subtract(vector, center) #traslation
    scaled_offset = vector2_scale(offset_vector, scale_factor) 
    scaled_vector = vector2_add(center, scaled_offset)
    return scaled_vector


def make_vec_proyection_y3d():
    pass


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
    
    gloom_shader = load_shader("0", "shaders/glsl330/bloom.fs");

    set_shader_value(gloom_shader, get_shader_location(gloom_shader,"size"), Vector2(SCREEN_WIDTH, SCREEN_HEIGHT) , ShaderUniformDataType.SHADER_UNIFORM_VEC2)
    set_shader_value(gloom_shader, get_shader_location(gloom_shader,"samples"), ffi.new("float *", 5.0) , ShaderUniformDataType.SHADER_UNIFORM_FLOAT)
    set_shader_value(gloom_shader, get_shader_location(gloom_shader,"quality"), ffi.new("float *", 1.8) , ShaderUniformDataType.SHADER_UNIFORM_FLOAT)


    render_texture = load_render_texture(SCREEN_WIDTH, SCREEN_HEIGHT)
    # Main game loop
    while not window_should_close():
        # LOOP SETTINGS BEFORE START THE RENDERING - BEGIN_DRAWING

        if is_key_pressed(KeyboardKey.KEY_RIGHT):
            if world_idx == len(worlds) - 1:
                world_idx = 0
            else:
                world_idx+=1
        elif is_key_pressed(KeyboardKey.KEY_LEFT):
            if world_idx == 0:
                world_idx = len(worlds) - 1
            else:
                world_idx-=1
        
        begin_drawing()

        begin_texture_mode(render_texture)
        clear_background(BLACK)
        # camera.rotation+=0.1
        begin_mode_2d(camera)
        draw_circle(int(SCREEN_CENTER.x), int(SCREEN_CENTER.y), 1, GREEN)
        draw_world(worlds[world_idx], TempestColors.BLUE_NEON)
        end_mode_2d()
        end_texture_mode()

        begin_shader_mode(gloom_shader) 
        draw_texture_rec(render_texture.texture, Rectangle(0,0, render_texture.texture.width, -render_texture.texture.height),Vector2(0,0), WHITE)
        end_shader_mode()
        draw_fps(0, 0)
        end_drawing()

    close_window()


if __name__ == "__main__":
    main()
