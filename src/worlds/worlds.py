from typing import List
from pydantic import BaseModel


# TYPE USED TO STORE LEVELS DATA
# https://arcarc.xmission.com/Web%20Archives/ionpool.net%20(Dec-31-2020)/arcade/tempest_code_project/TempEd/technical/technical.html
class LevelData(BaseModel):
    x: List[int]  # The x-coordinates of the points in the level.
    # In the original, these were in the range 0-255, representing positions in 2D space.

    y: List[int]  # The y-coordinates of the points in the level.
    # In the original arcade game, a 125% y-scale was applied to everything drawn, meaning the y-values were stretched.

    # TODO: optimize world generation saving the center proyection instead of computing it each time
    px: List[int] = [] # The proyection y relative to the center of the screen using a scale e.g 0.12 -> 12% of x

    py: List[int] = [] # The proyection y relative to the center of the screen using a scale e.g 0.12 -> 12% of y

    y3d: int  # The 3D y-offset (camera height), used to adjust the perspective of the levels.
    # In the original game, this offset was used to position the viewpoint relative to the level geometry.

    is_loop: bool  # The open/close status of the level.
    # In a closed level (with 16 sectors), the path loops. In an open level (with 15 sectors), it doesn’t.

    start_idx: int

circle_world = LevelData(
    x=[550.0, 530.0, 476.0, 395.0, 300.0, 205.0, 124.0, 70.0, 50.0, 70.0, 124.0, 205.0, 300.0, 395.0, 476.0, 530.0],
    y=[400.0, 495.0, 576.0, 630.0, 650.0, 630.0, 576.0, 495.0, 400.0, 305.0, 224.0, 170.0, 150.0, 170.0, 224.0, 305.0],
    y3d=80,
    is_loop=True,
    start_idx=4,
)

square_world = LevelData(
    x=[50.0, 50.0, 50.0, 50.0, 50.0, 175.0, 300.0, 425.0, 550.0, 550.0, 550.0, 550.0, 550.0, 425.0, 300.0, 175.0],
    y=[650.0, 525.0, 400.0, 275.0, 150.0, 150.0, 150.0, 150.0, 150.0, 275.0, 400.0, 525.0, 650.0, 650.0, 650.0, 650.0],
    y3d=70,
    is_loop=True,
    start_idx=14,
)


plus_world = LevelData(
    x=[175.0, 50.0, 50.0, 50.0, 175.0, 175.0, 300.0, 425.0, 425.0, 550.0, 550.0, 550.0, 425.0, 425.0, 300.0, 175.0],
    y=[525.0, 525.0, 400.0, 275.0, 275.0, 150.0, 150.0, 150.0, 275.0, 275.0, 400.0, 525.0, 525.0, 650.0, 650.0, 650.0],
    y3d=70,
    is_loop=True,
    start_idx=14,
)

peanut_world = LevelData(
    x = [260.0, 180.0, 80.0, 40.0, 40.0, 80.0, 180.0, 260.0, 340.0, 420.0, 520.0, 560.0, 560.0, 520.0, 420.0, 340.0],
    y = [490.0, 535.0, 505.0, 445.0, 355.0, 295.0, 265.0, 310.0, 310.0, 265.0, 295.0, 355.0, 445.0, 505.0, 535.0, 490.0],
    y3d=45,
    is_loop=True,
    start_idx=0,
)

cross_world = LevelData(
    x=[260.0, 220.0, 140.0, 20.0, 20.0, 140.0, 220.0, 260.0, 340.0, 380.0, 460.0, 580.0, 580.0, 460.0, 380.0, 340.0],
    y=[680.0, 560.0, 480.0, 440.0, 360.0, 320.0, 240.0, 120.0, 120.0, 240.0, 320.0, 360.0, 440.0, 480.0, 560.0, 680.0],
    y3d=70,
    is_loop=True,
    start_idx=0,
)

triangle_world = LevelData(
    x=[164.0, 100.0, 140.0, 180.0, 220.0, 260.0, 300.0, 340.0, 380.0, 420.0, 460.0, 500.0, 436.0, 364.0, 300.0, 236.0],
    y=[598.0, 598.0, 499.0, 400.0, 301.0, 202.0, 103.0, 202.0, 301.0, 400.0, 499.0, 598.0, 598.0, 598.0, 598.0, 598.0],
    y3d=40,
    is_loop=True,
    start_idx=14,
)

clover_world = LevelData(
    x=[75.0, 50.0, 175.0, 50.0, 75.0, 238.0, 300.0, 362.0, 525.0, 550.0, 425.0, 550.0, 525.0, 362.0, 300.0, 238.0],
    y=[625.0, 462.0, 400.0, 338.0, 175.0, 150.0, 275.0, 150.0, 175.0, 338.0, 400.0, 462.0, 625.0, 650.0, 525.0, 650.0],
    y3d=55,
    is_loop=True,
    start_idx=13,
)

vee_world = LevelData(
    x=[540.0, 510.0, 480.0, 450.0, 420.0, 390.0, 360.0, 330.0, 270.0, 240.0, 210.0, 180.0, 150.0, 120.0, 90.0, 60.0],
    y=[140.0, 205.0, 270.0, 335.0, 400.0, 465.0, 530.0, 595.0, 595.0, 530.0, 465.0, 400.0, 335.0, 270.0, 205.0, 140.0],
    y3d=-90,
    is_loop=False,
    start_idx=8,
)

steps_world = LevelData(
    x=[580.0, 580.0, 500.0, 500.0, 420.0, 420.0, 340.0, 340.0, 260.0, 260.0, 180.0, 180.0, 100.0, 100.0, 20.0, 20.0],
    y=[265.0, 355.0, 355.0, 445.0, 445.0, 535.0, 535.0, 625.0, 625.0, 535.0, 535.0, 445.0, 445.0, 355.0, 355.0, 265.0],
    y3d=-200,
    is_loop=False,
    start_idx=8,
)

u_shape_world = LevelData(
    x=[545.0, 545.0, 545.0, 545.0, 538.0, 492.0, 422.0, 335.0, 265.0, 178.0, 108.0, 62.0, 55.0, 55.0, 55.0, 55.0],
    y=[175.0, 265.0, 355.0, 445.0, 535.0, 625.0, 692.0, 715.0, 715.0, 692.0, 625.0, 535.0, 445.0, 355.0, 265.0, 175.0],
    y3d=150,
    is_loop=False,
    start_idx=8,
)

line_world = LevelData(
    x=[592.0, 553.0, 514.0, 475.0, 436.0, 397.0, 358.0, 319.0, 281.0, 242.0, 203.0, 164.0, 125.0, 86.0, 47.0, 8.0],
    y=[560.0, 560.0, 560.0, 560.0, 560.0, 560.0, 560.0, 560.0, 560.0, 560.0, 560.0, 560.0, 560.0, 560.0, 560.0, 560.0],
    y3d=-170,
    is_loop=False,
    start_idx=8,
)

heart_world = LevelData(
    x=[380.0, 500.0, 540.0, 540.0, 500.0, 420.0, 300.0, 180.0, 100.0, 60.0, 60.0, 100.0, 220.0, 280.0, 300.0, 320.0],
    y=[190.0, 201.0, 330.0, 470.0, 575.0, 645.0, 680.0, 645.0, 575.0, 470.0, 330.0, 201.0, 190.0, 295.0, 435.0, 295.0],
    y3d=215,
    is_loop=True,
    start_idx=6,
)

star_world = LevelData(
    x=[165.0, 75.0, 120.0, 75.0, 165.0, 210.0, 300.0, 390.0, 435.0, 525.0, 480.0, 525.0, 435.0, 390.0, 300.0, 210.0],
    y=[543.0, 510.0, 400.0, 290.0, 257.0, 158.0, 213.0, 158.0, 257.0, 290.0, 400.0, 510.0, 543.0, 642.0, 587.0, 642.0],
    y3d=60,
    is_loop=True,
    start_idx=14,
)

w_shape_world = LevelData(
    x=[580.0, 545.0, 534.0, 513.0, 464.0, 394.0, 352.0, 321.0, 279.0, 248.0, 206.0, 136.0, 87.0, 66.0, 55.0, 20.0],
    y=[295.0, 365.0, 452.0, 529.0, 582.0, 582.0, 540.0, 470.0, 470.0, 540.0, 582.0, 582.0, 529.0, 452.0, 365.0, 295.0],
    y3d=-170,
    is_loop=False,
    start_idx=8,
)

broken_v_world = LevelData(
    x=[580.0, 562.0, 545.0, 527.0, 440.0, 398.0, 373.0, 338.0, 265.0, 213.0, 171.0, 143.0, 125.0, 108.0, 73.0, 20.0],
    y=[120.0, 211.0, 295.0, 393.0, 376.0, 452.0, 540.0, 592.0, 575.0, 627.0, 540.0, 470.0, 365.0, 295.0, 225.0, 155.0],
    y3d=-90,
    is_loop=False,
    start_idx=8,
)

infinity_world = LevelData(
    x=[300.0, 348.0, 444.0, 540.0, 588.0, 540.0, 444.0, 348.0, 300.0, 252.0, 156.0, 60.0, 12.0, 60.0, 156.0, 252.0],
    y=[400.0, 290.0, 235.0, 290.0, 400.0, 510.0, 565.0, 510.0, 400.0, 290.0, 235.0, 290.0, 400.0, 510.0, 565.0, 510.0],
    y3d=0,
    is_loop=True,
    start_idx=1,
)
