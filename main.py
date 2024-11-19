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
from src.shared.input_manager import InputManager
from src.sounds import SoundManager
import os, platform, asyncio


def init_gloom_shader() -> Shader:
    # Its important to use os.path with dirname(__file__) to make files reachables from .exe/.bin builds.
    glsl_version = "300es" if platform.system() == "Emscripten" else "330"
    shader_path = os.path.join(os.path.dirname(__file__), f"assets/shaders/glsl{glsl_version}/bloom.fs")
    gloom_shader = load_shader("0", shader_path)
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

class Renderer:
    def __init__(self, game):
        self.game = game
        self.camera = init_2d_camera()
        self.gloom_shader = init_gloom_shader()
        self.render_texture = load_render_texture(SCREEN_WIDTH, SCREEN_HEIGHT)
        set_texture_filter(self.render_texture.texture, TextureFilter.TEXTURE_FILTER_BILINEAR)
        self.fullscreen = False
        self.rt_origin = Vector2(0,0)
        self.rt_source = Rectangle()
        self.rt_dest = Rectangle()
        self.resize()

    def resize(self):
        aspect = get_screen_height() / self.render_texture.texture.height
        self.rt_source = Rectangle(0, 0, self.render_texture.texture.width, -self.render_texture.texture.height)
        self.rt_dest = Rectangle((get_screen_width()-self.render_texture.texture.width*aspect)/2, 0, self.render_texture.texture.width * aspect, get_screen_height())


    def destroy(self):
        unload_render_texture(self.render_texture)
        unload_shader(self.gloom_shader)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        toggle_borderless_windowed()
        begin_drawing()
        end_drawing()
        self.resize()

    def render_frame(self):
        begin_drawing()
        clear_background(BLACK)
        begin_texture_mode(self.render_texture)
        clear_background(BLACK)
        begin_mode_2d(self.camera)

        # Draw game
        self.game.draw_frame()

        end_mode_2d()
        end_texture_mode()

        begin_shader_mode(self.gloom_shader)
        draw_texture_pro(self.render_texture.texture, self.rt_source, self.rt_dest, self.rt_origin,0,WHITE)

        end_shader_mode()

        draw_fps(0, 0)
        end_drawing()


async def main():

    # Engine setup
    setup_window()

    if platform.system() != "Emscripten":  # audio does not work on current version of emscripten
        init_audio_device()

    sound_volume = 0.7
    sound_manager = SoundManager(sound_volume)
    sound_manager.load_sounds()

    input_manager = InputManager()

    game = Game(sound_manager, input_manager)

    renderer = Renderer(game)

    # Main game loop
    while not window_should_close():
        if is_key_pressed(KeyboardKey.KEY_F) or get_touch_point_count()>0 and not renderer.fullscreen:
            renderer.toggle_fullscreen()
        # Update game
        game.update_frame()
        input_manager.update_touch_input()
        renderer.resize() # shouldn't be necessary every frame but Linux GLFW seems to need it!
        renderer.render_frame()
        await asyncio.sleep(0)


    renderer.destroy()
    unload_image(icon)
    sound_manager.unload_sounds()
    close_audio_device()
    close_window()


if __name__ == "__main__":
    asyncio.run(main())
