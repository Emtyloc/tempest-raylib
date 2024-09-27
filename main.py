from pyray import *
from worlds import *

def draw_hole_points(level_data: LevelData):
    for x, y in zip(level_data.x, level_data.y):
        draw_circle(int(x), int(y), 1, RED)


def main():

    # SCREEN SETTINGS
    SCREEN_WIDTH: int = 600
    SCREEN_HEIGHT: int = 800
    TARGET_FPS = 60
    init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Tempest Raylib")
    set_target_fps(TARGET_FPS)

    # CAMERA SETTINGS
    screen_center = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    camera = Camera2D()
    camera.target = screen_center  # WHERE THE CAMARA IS LOCATED INSIDE THE GAME
    camera.offset = (
        screen_center  # WHERE THE CAMERA IMAGE IS DISPLAYED IN THE PLAYER SCREEN
    )
    camera.rotation = 0
    camera.zoom = 1

    world_idx = 0
    worlds = [circle_world, square_world, plus_world, peanut_world, cross_world, triangle_world, clover_world, vee_world, steps_world, u_shape_world]
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
        clear_background(BLACK)
        draw_fps(0, 0)
        # camera.rotation+=0.1
        begin_mode_2d(camera)
        draw_circle(int(screen_center.x), int(screen_center.y), 1, GREEN)
        draw_hole_points(worlds[world_idx])
        end_mode_2d()
        end_drawing()

    close_window()


if __name__ == "__main__":
    main()
