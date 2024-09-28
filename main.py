from pyray import *
from worlds import *

#SETTINGS
SCREEN_WIDTH: int = 600
SCREEN_HEIGHT: int = 800
TARGET_FPS = 60
screen_center = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)



def draw_world(level_data: LevelData):
    for i in range(16):
        # Draw main figure points
        pers_scale = 0.12
        custom_blue = Color(16, 14, 100, 255)
        border_blue = Color(27, 38, 169, 255)
        draw_circle(int(level_data.x[i]), int(level_data.y[i]), 2, border_blue)
        # draw_circle(int(screen_center.x + (level_data.x[i] - screen_center.x)*pers_scale), int(screen_center.y + level_data.y3d + (level_data.y[i] - screen_center.y + level_data.y3d)*pers_scale), 1, SKYBLUE)
        org_vec = Vector2(level_data.x[i],level_data.y[i])
        des_vec = Vector2(int(screen_center.x + (level_data.x[i] - screen_center.x)*pers_scale), int(screen_center.y + level_data.y3d + (level_data.y[i] - screen_center.y + level_data.y3d)*pers_scale))
        draw_line_ex(org_vec, des_vec, 2, custom_blue)
        # draw_line_ex(org_vec, des_vec, 2, SKYBLUE)
        # draw_line(level_data.x[i],level_data.y[i], int(screen_center.x + (level_data.x[i] - screen_center.x)*pers_scale), int(screen_center.y + level_data.y3d + (level_data.y[i] - screen_center.y + level_data.y3d)*pers_scale), SKYBLUE)
        if i > 0:
            # draw world figure
            org_vec = Vector2(level_data.x[i], level_data.y[i])
            des_vec = Vector2(level_data.x[i-1], level_data.y[i-1])
            draw_line_ex(org_vec, des_vec, 2, border_blue)
            # draw_line(level_data.x[i],level_data.y[i], level_data.x[i-1], level_data.y[i-1], BLUE)
            org_vec = Vector2(int(screen_center.x + (level_data.x[i] - screen_center.x)*pers_scale), int(screen_center.y + level_data.y3d + (level_data.y[i] - screen_center.y + level_data.y3d)*pers_scale))
            des_vec = Vector2(int(screen_center.x + (level_data.x[i-1] - screen_center.x)*pers_scale), int(screen_center.y + level_data.y3d + (level_data.y[i-1] - screen_center.y + level_data.y3d)*pers_scale))
            draw_line_ex(org_vec, des_vec, 1, border_blue)
            # draw_line(int(screen_center.x + (level_data.x[i] - screen_center.x)*pers_scale), int(screen_center.y + level_data.y3d + (level_data.y[i] - screen_center.y + level_data.y3d)*pers_scale), int(screen_center.x + (level_data.x[i-1] - screen_center.x)*pers_scale), int(screen_center.y + level_data.y3d + (level_data.y[i-1] - screen_center.y + level_data.y3d)*pers_scale), BLUE)
            # draw world perspective
            # draw perspective lines

    else:
        if not level_data.open_state:
            org_vec = Vector2(level_data.x[0],level_data.y[0])
            des_vec = Vector2(level_data.x[-1], level_data.y[-1])
            draw_line_ex(org_vec, des_vec, 2, border_blue)
            # draw_line(level_data.x[0],level_data.y[0], level_data.x[-1], level_data.y[-1], BLUE)
            org_vec = Vector2(int(screen_center.x + (level_data.x[0] - screen_center.x)*pers_scale), int(screen_center.y + level_data.y3d + (level_data.y[0] - screen_center.y + level_data.y3d)*pers_scale))
            des_vec = Vector2(int(screen_center.x + (level_data.x[-1] - screen_center.x)*pers_scale), int(screen_center.y + level_data.y3d + (level_data.y[-1] - screen_center.y + level_data.y3d)*pers_scale))
            draw_line_ex(org_vec, des_vec, 1, border_blue)
            # draw_line(int(screen_center.x + (level_data.x[0] - screen_center.x)*pers_scale), int(screen_center.y + level_data.y3d + (level_data.y[0] - screen_center.y + level_data.y3d)*pers_scale), int(screen_center.x + (level_data.x[-1] - screen_center.x)*pers_scale), int(screen_center.y + level_data.y3d + (level_data.y[-1] - screen_center.y + level_data.y3d)*pers_scale), BLUE)



def main():
    
    init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Tempest Raylib")
    set_target_fps(TARGET_FPS)

    # CAMERA SETTINGS
   
    camera = Camera2D()
    camera.target = screen_center  # WHERE THE CAMARA IS LOCATED INSIDE THE GAME
    camera.offset = (
        screen_center  # WHERE THE CAMERA IMAGE IS DISPLAYED IN THE PLAYER SCREEN
    )
    camera.rotation = 0
    camera.zoom = 1

    world_idx = 0
    worlds = [circle_world, square_world, plus_world, peanut_world, cross_world, triangle_world, clover_world, vee_world, steps_world, u_shape_world, line_world, heart_world, star_world, w_shape_world, broken_v_world, infinity_world]
    
    gloom_shader = load_shader("0", "shaders/glsl330/bloom.fs");
    
    set_shader_value(gloom_shader, get_shader_location_attrib(gloom_shader,"size"), Vector2(SCREEN_WIDTH, SCREEN_HEIGHT), ShaderUniformDataType.SHADER_UNIFORM_VEC2)

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
        draw_circle(int(screen_center.x), int(screen_center.y), 1, GREEN)
        draw_world(worlds[world_idx])
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
