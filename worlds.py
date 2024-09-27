from typing import List
from pydantic import BaseModel


# TYPE USED TO STORE LEVELS DATA
# https://arcarc.xmission.com/Web%20Archives/ionpool.net%20(Dec-31-2020)/arcade/tempest_code_project/TempEd/technical/technical.html
class LevelData(BaseModel):
    x: List[int]  # The x-coordinates of the points in the level.
    # In the original, these were in the range 0-255, representing positions in 2D space.

    y: List[int]  # The y-coordinates of the points in the level.
    # In the original arcade game, a 125% y-scale was applied to everything drawn, meaning the y-values were stretched.

    # angle: List[int]  # The angles of the sectors in the level.
    # Originally in the range 0-15, where each value represents 0-360 degrees (15 equals 360 degrees).
    # These values might have been manually adjusted in the original levels.

    scale: int  # The scale of the level, or more precisely "one-over the scale" — smaller values produce larger levels.
    # The scale values ranged from 10 to 28 in the original levels (1-255 overall).

    y3d: int  # The 3D y-offset (camera height), used to adjust the perspective of the levels.
    # In the original game, this offset was used to position the viewpoint relative to the level geometry.

    y2d: int  # The low byte of the 2D y-offset.
    y2db: int  # The high byte of the 2D y-offset, a signed value (usually between -2 and +2).
    # These two combine to form a 16-bit value: y_offset = y2db * 256 + y2d

    open_state: bool  # The open/close status of the level.
    # In a closed level (with 16 sectors), the path loops. In an open level (with 15 sectors), it doesn’t.

    fscale: int  # The low byte of the flipper scale. Flippers (enemies) use this value to scale their size when flipping.
    fscale2: int  # The high byte of the flipper scale.
    # The full value is calculated as: flipper_scale = fscale2 * 128 + fscale
    # This value determines how flippers "shrink" or "grow" when rotating through sectors.

    # Other relevant comments:
    # - The original level data was stored in ROM files, and the levels were remapped to be played in a different order than stored.
    # - Some of these fields were likely limited due to memory and processing constraints on the arcade hardware, which may not be necessary for a modern recreation.


circle_world = LevelData(
    x = [500.0, 484.0, 441.0, 376.0, 300.0, 224.0, 159.0, 116.0, 100.0, 116.0, 159.0, 224.0, 300.0, 376.0, 441.0, 484.0],
    y = [400.0, 476.0, 541.0, 584.0, 600.0, 584.0, 541.0, 476.0, 400.0, 324.0, 259.0, 216.0, 200.0, 216.0, 259.0, 324.0],
    scale=1,
    y3d=0,
    y2d=0,
    y2db=0,
    open_state=False,
    fscale=1,
    fscale2=1,
)

square_world = LevelData(
    x = [100.0, 100.0, 100.0, 100.0, 100.0, 200.0, 300.0, 400.0, 500.0, 500.0, 500.0, 500.0, 500.0, 400.0, 300.0, 200.0],
    y = [600.0, 500.0, 400.0, 300.0, 200.0, 200.0, 200.0, 200.0, 200.0, 300.0, 400.0, 500.0, 600.0, 600.0, 600.0, 600.0],
    scale=1,
    y3d=0,
    y2d=0,
    y2db=0,
    open_state=False,
    fscale=1,
    fscale2=1,
)


plus_world = LevelData(
    x = [200.0, 100.0, 100.0, 100.0, 200.0, 200.0, 300.0, 400.0, 400.0, 500.0, 500.0, 500.0, 400.0, 400.0, 300.0, 200.0],
    y = [500.0, 500.0, 400.0, 300.0, 300.0, 200.0, 200.0, 200.0, 300.0, 300.0, 400.0, 500.0, 500.0, 600.0, 600.0, 600.0],
    scale=1,
    y3d=0,
    y2d=0,
    y2db=0,
    open_state=False,
    fscale=1,
    fscale2=1,
)

peanut_world = LevelData(
    x = [260.0, 180.0, 80.0, 40.0, 40.0, 80.0, 180.0, 260.0, 340.0, 420.0, 520.0, 560.0, 560.0, 520.0, 420.0, 340.0],
    y = [490.0, 535.0, 505.0, 445.0, 355.0, 295.0, 265.0, 310.0, 310.0, 265.0, 295.0, 355.0, 445.0, 505.0, 535.0, 490.0],
    scale=1,
    y3d=0,
    y2d=0,
    y2db=0,
    open_state=False,
    fscale=1,
    fscale2=1,
)

cross_world = LevelData(
    x=[270.0, 240.0, 180.0, 90.0, 90.0, 180.0, 240.0, 270.0, 330.0, 360.0, 420.0, 510.0, 510.0, 420.0, 360.0, 330.0],
    y=[610.0, 520.0, 460.0, 430.0, 370.0, 340.0, 280.0, 190.0, 190.0, 280.0, 340.0, 370.0, 430.0, 460.0, 520.0, 610.0],
    scale=1,
    y3d=0,
    y2d=0,
    y2db=0,
    open_state=False,
    fscale=1,
    fscale2=1,
)

triangle_world = LevelData(
    x=[181.0, 125.0, 160.0, 195.0, 230.0, 265.0, 300.0, 335.0, 370.0, 405.0, 440.0, 475.0, 419.0, 356.0, 300.0, 244.0],
    y=[568.0, 568.0, 484.0, 400.0, 316.0, 232.0, 148.0, 232.0, 316.0, 400.0, 484.0, 568.0, 568.0, 568.0, 568.0, 568.0],
    scale=1,
    y3d=0,
    y2d=0,
    y2db=0,
    open_state=False,
    fscale=1,
    fscale2=1,
)

clover_world = LevelData(
    x=[120.0, 100.0, 200.0, 100.0, 120.0, 250.0, 300.0, 350.0, 480.0, 500.0, 400.0, 500.0, 480.0, 350.0, 300.0, 250.0],
    y=[580.0, 450.0, 400.0, 350.0, 220.0, 200.0, 300.0, 200.0, 220.0, 350.0, 400.0, 450.0, 580.0, 600.0, 500.0, 600.0],
    scale=1,
    y3d=0,
    y2d=0,
    y2db=0,
    open_state=False,
    fscale=1,
    fscale2=1,
)

vee_world = LevelData(
    x=[540.0, 510.0, 480.0, 450.0, 420.0, 390.0, 360.0, 330.0, 270.0, 240.0, 210.0, 180.0, 150.0, 120.0, 90.0, 60.0],
    y=[180.0, 235.0, 290.0, 345.0, 400.0, 455.0, 510.0, 565.0, 565.0, 510.0, 455.0, 400.0, 345.0, 290.0, 235.0, 180.0],
    scale=1,
    y3d=0,
    y2d=0,
    y2db=0,
    open_state=False,
    fscale=1,
    fscale2=1,
)

steps_world = LevelData(
    x=[580.0, 580.0, 500.0, 500.0, 420.0, 420.0, 340.0, 340.0, 260.0, 260.0, 180.0, 180.0, 100.0, 100.0, 20.0, 20.0],
    y=[292.0, 364.0, 364.0, 436.0, 436.0, 508.0, 508.0, 580.0, 580.0, 508.0, 508.0, 436.0, 436.0, 364.0, 364.0, 292.0],
    scale=1,
    y3d=0,
    y2d=0,
    y2db=0,
    open_state=False,
    fscale=1,
    fscale2=1,
)

u_shape_world = LevelData(
    x=[510.0, 510.0, 510.0, 510.0, 504.0, 465.0, 405.0, 330.0, 270.0, 195.0, 135.0, 96.0, 90.0, 90.0, 90.0, 90.0],
    y=[225.0, 295.0, 365.0, 435.0, 505.0, 575.0, 627.0, 645.0, 645.0, 627.0, 575.0, 505.0, 435.0, 365.0, 295.0, 225.0],
    scale=1,
    y3d=0,
    y2d=0,
    y2db=0,
    open_state=False,
    fscale=1,
    fscale2=1,
)

