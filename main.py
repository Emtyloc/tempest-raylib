# /// script
# dependencies = [
#     "cffi",
#     "raylib"
# ]
# ///
from pyray import *
from raylib import ffi
from src.shared import TempestColors, SCREEN_CENTER, SCREEN_HEIGHT, SCREEN_WIDTH, TARGET_FPS
from src.game import Game
from src.sounds import SoundManager
import os, platform, asyncio


def init_gloom_shader() -> Shader:
    # Its important to use os.path with dirname(__file__) to make files reachables from .exe/.bin builds.
    shader_path = os.path.join(os.path.dirname(__file__), "assets/shaders/glsl330/bloom.fs")
    gloom_shader = load_shader("0", shader_path);
    set_shader_value(gloom_shader, get_shader_location(gloom_shader,"size"), Vector2(SCREEN_WIDTH, SCREEN_HEIGHT) , ShaderUniformDataType.SHADER_UNIFORM_VEC2)
    set_shader_value(gloom_shader, get_shader_location(gloom_shader,"samples"), ffi.new("float *", 11.0) , ShaderUniformDataType.SHADER_UNIFORM_FLOAT)
    set_shader_value(gloom_shader, get_shader_location(gloom_shader,"quality"), ffi.new("float *", 1.0) , ShaderUniformDataType.SHADER_UNIFORM_FLOAT)
    return gloom_shader

icon = load_image(os.path.join(os.path.dirname(__file__), "icon.png"))
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


async def main():

    # Engine setup
    setup_window()
    camera = init_2d_camera()
    gloom_shader = init_gloom_shader()
    render_texture = load_render_texture(SCREEN_WIDTH, SCREEN_HEIGHT)

    if platform.system() != "Emscripten":  # audio does not work on current version of emscripten
        init_audio_device()

    sound_volume = 0.7
    sound_manager = SoundManager(sound_volume)
    sound_manager.load_sounds()

    game = Game(sound_manager)

    # Main game loop
    while not window_should_close():
        
        # Update game
        game.update_frame()
        
        begin_drawing()

        begin_texture_mode(render_texture)
        
        clear_background(BLACK)
        begin_mode_2d(camera)
        
        # Draw game
        game.draw_frame()

        end_mode_2d()
        end_texture_mode()

        begin_shader_mode(gloom_shader) 
        draw_texture_rec(render_texture.texture, Rectangle(0,0, render_texture.texture.width, -render_texture.texture.height),Vector2(0,0), WHITE)
        end_shader_mode()

        draw_fps(0, 0)
        end_drawing()
        await asyncio.sleep(0)

    unload_shader(gloom_shader)
    unload_render_texture(render_texture)
    unload_image(icon)
    sound_manager.unload_sounds()
    close_audio_device()
    close_window()


if __name__ == "__main__":
    asyncio.run(main())
