from pyray import *
from pydantic import BaseModel, Field
from typing import List, Annotated


# DEFINE 8-BITS NUMBERS TYPES
# UNSIGNED - BETWEEN 0 AND 255
uint8 = Annotated[int, Field(ge=0, le=255)]
# SIGNED - BETWEEN -128 AND 255
sint8 = Annotated[int, Field(ge=-128, le=127)]


# TYPE USED TO STORE LEVELS DATA
# https://arcarc.xmission.com/Web%20Archives/ionpool.net%20(Dec-31-2020)/arcade/tempest_code_project/TempEd/technical/technical.html
class LevelData(BaseModel):
    x: List[uint8]  # the x-coordinates of the points in the level.
    y: List[uint8]  # the y-coordinates of the points in the level.
    # x & y are in the range 0-255.
    # Note that the arcade game applies a y-scale of 125% to everything drawn.

    angle: List[uint8]  # the angles of the sectors in the level.
    # Angle is in the range 0-15 (representing 0-360 degrees).

    scale: uint8  # the scale of the level, or more accurately one-over the scale since small values give big levels.
    # Scale is in the range 1-255, although 10-28 is the range of the original levels.

    y3d: uint8  # the 3D y-offset, or 'camera height' for the levels.
    y2d: uint8  # 'Low' byte of 2D y-offset.
    y2db: sint8  # 'High' byte of 2D y-offset. is (usually) in the range -2 to +2.
    # The 2D y-offset is stored as a 16-bit value, i.e. yoffset = y2db*256 + y2d

    open_state: bool  # open/close status of the level
    # A closed level has 16 sectors and is looped. An open level has 15 sectors and does not loop.

    fscale: uint8  # 'Low' byte of flipper scale.
    fscale2: uint8  # 'High' byte of flipper scale.
    # The 'flipper scale' is the value used to scale the flippers when they are in the act of flipping.
    # When flippers are lying fully in a sector, they take their shape from that sector's co-ordinates.
    # Like the level scale, small values mean big flippers.
    # This was the most troublesome piece of data to work out.
    # Although it seems to be a 16-bit value, it is not stored in the usual way.
    # Instead, fscale only represents the first 7 bits, and fscale2 the rest. So the full value is recovered as:

    # fs = fscale2*128 + fscale

    # TempEd calculates this value based on the average sector width of the level (actually, one-over the average width).


level = LevelData(
    x=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    y=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    angle=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    scale=1,
    y3d=0,
    y2d=0,
    y2db=0,
    open_state=True,
    fscale=0,
    fscale2=0,
)


def main():

    # SCREEN SETTINGS
    SCREEN_WIDTH: int = 480
    SCREEN_HEIGHT: int = 640
    TARGET_FPS = 60
    init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Tempest Raylib")
    set_target_fps(TARGET_FPS)

    # CAMERA SETTINGS
    camera = Camera2D()
    camera.target = Vector2(
        SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
    )  # WHERE THE CAMARA IS LOCATED INSIDE THE GAME
    camera.offset = Vector2(
        SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
    )  # WHERE THE CAMERA IMAGE IS DISPLAYED IN THE PLAYER SCREEN
    camera.rotation = 0
    camera.zoom = 1

    # Main game loop
    while not window_should_close():
        # LOOP SETTINGS BEFORE START THE RENDERING - BEGIN_DRAWING
        begin_drawing()
        clear_background(BLACK)
        begin_mode_2d(camera)
        end_mode_2d()
        end_drawing()

    close_window()


if __name__ == "__main__":
    main()
