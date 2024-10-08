from dataclasses import dataclass
from ..utils import Vec2
from pyray import *
from ..shared import SCREEN_CENTER


# TYPE USED TO STORE LEVELS DATA
# https://arcarc.xmission.com/Web%20Archives/ionpool.net%20(Dec-31-2020)/arcade/tempest_code_project/TempEd/technical/technical.html
@dataclass
class WorldData:
    borders: list[Vec2]

    proyections: list[Vec2] # The proyection y relative to the center of the screen using a scale e.g 0.12 -> 12% of y

    y3d: int  # The 3D y-offset (camera height), used to adjust the perspective of the levels.
    # In the original game, this offset was used to position the viewpoint relative to the level geometry.

    is_loop: bool  # The open/close status of the level.
    # In a closed level (with 16 sectors), the path loops. In an open level (with 15 sectors), it doesn’t.

    start_idx: int


circle_world = WorldData(
    borders=[Vec2(550, 400), Vec2(530, 495), Vec2(476, 576), Vec2(395, 630), Vec2(300, 650), Vec2(204, 630), Vec2(123, 576), Vec2(69, 495), Vec2(50, 400), Vec2(69, 304), Vec2(123, 223), Vec2(204, 169), Vec2(299, 150), Vec2(395, 169), Vec2(476, 223), Vec2(530, 304)],
    proyections=[Vec2(330, 480), Vec2(327, 491), Vec2(321, 501), Vec2(311, 507), Vec2(300, 510), Vec2(288, 507), Vec2(278, 501), Vec2(272, 491), Vec2(270, 480), Vec2(272, 468), Vec2(278, 458), Vec2(288, 452), Vec2(299, 450), Vec2(311, 452), Vec2(321, 458), Vec2(327, 468)],
    y3d=80,
    is_loop=True,
    start_idx=4,
)

square_world = WorldData(
    borders=[Vec2(50, 650), Vec2(50, 525), Vec2(50, 400), Vec2(50, 275), Vec2(50, 150), Vec2(175, 150), Vec2(300, 150), Vec2(425, 150), Vec2(550, 150), Vec2(550, 275), Vec2(550, 400), Vec2(550, 525), Vec2(550, 650), Vec2(425, 650), Vec2(300, 650), Vec2(175, 650)],
    proyections=[Vec2(270, 510), Vec2(270, 495), Vec2(270, 480), Vec2(270, 465), Vec2(270, 450), Vec2(285, 450), Vec2(300, 450), Vec2(315, 450), Vec2(330, 450), Vec2(330, 465), Vec2(330, 480), Vec2(330, 495), Vec2(330, 510), Vec2(315, 510), Vec2(300, 510), Vec2(285, 510)],
    y3d=70,
    is_loop=True,
    start_idx=14,
)


plus_world = WorldData(
    borders=[Vec2(175, 525), Vec2(50, 525), Vec2(50, 400), Vec2(50, 275), Vec2(175, 275), Vec2(175, 150), Vec2(300, 150), Vec2(425, 150), Vec2(425, 275), Vec2(550, 275), Vec2(550, 400), Vec2(550, 525), Vec2(425, 525), Vec2(425, 650), Vec2(300, 650), Vec2(175, 650)],
    proyections=[Vec2(285, 485), Vec2(270, 485), Vec2(270, 470), Vec2(270, 455), Vec2(285, 455), Vec2(285, 440), Vec2(300, 440), Vec2(315, 440), Vec2(315, 455), Vec2(330, 455), Vec2(330, 470), Vec2(330, 485), Vec2(315, 485), Vec2(315, 500), Vec2(300, 500), Vec2(285, 500)],
    y3d=70,
    is_loop=True,
    start_idx=14,
)

peanut_world = WorldData(
    borders=[Vec2(260, 490), Vec2(180, 535), Vec2(80, 505), Vec2(40, 445), Vec2(40, 355), Vec2(80, 295), Vec2(180, 265), Vec2(260, 310), Vec2(340, 310), Vec2(420, 265), Vec2(520, 295), Vec2(560, 355), Vec2(560, 445), Vec2(520, 505), Vec2(420, 535), Vec2(340, 490)],
    proyections=[Vec2(295, 455), Vec2(285, 461), Vec2(273, 457), Vec2(268, 450), Vec2(268, 439), Vec2(273, 432), Vec2(285, 428), Vec2(295, 434), Vec2(304, 434), Vec2(314, 428), Vec2(326, 432), Vec2(331, 439), Vec2(331, 450), Vec2(326, 457), Vec2(314, 461), Vec2(304, 455)],
    y3d=45,
    is_loop=True,
    start_idx=0,
)

cross_world = WorldData(
    borders=[Vec2(260, 680), Vec2(220, 560), Vec2(140, 480), Vec2(20, 440), Vec2(20, 360), Vec2(140, 320), Vec2(220, 240), Vec2(260, 120), Vec2(340, 120), Vec2(380, 240), Vec2(460, 320), Vec2(580, 360), Vec2(580, 440), Vec2(460, 480), Vec2(380, 560), Vec2(340, 680)],
    proyections=[Vec2(295, 503), Vec2(290, 489), Vec2(280, 479), Vec2(266, 474), Vec2(266, 465), Vec2(280, 460), Vec2(290, 450), Vec2(295, 436), Vec2(304, 436), Vec2(309, 450), Vec2(319, 460), Vec2(333, 465), Vec2(333, 474), Vec2(319, 479), Vec2(309, 489), Vec2(304, 503)],
    y3d=70,
    is_loop=True,
    start_idx=0,
)

triangle_world = WorldData(
    borders=[Vec2(164, 598), Vec2(100, 598), Vec2(140, 499), Vec2(180, 400), Vec2(220, 301), Vec2(260, 202), Vec2(300, 103), Vec2(340, 202), Vec2(380, 301), Vec2(420, 400), Vec2(460, 499), Vec2(500, 598), Vec2(436, 598), Vec2(364, 598), Vec2(300, 598), Vec2(236, 598)],
    proyections=[Vec2(283, 463), Vec2(276, 463), Vec2(280, 451), Vec2(285, 440), Vec2(290, 428), Vec2(295, 416), Vec2(300, 404), Vec2(304, 416), Vec2(309, 428), Vec2(314, 440), Vec2(319, 451), Vec2(324, 463), Vec2(316, 463), Vec2(307, 463), Vec2(300, 463), Vec2(292, 463)],
    y3d=40,
    is_loop=True,
    start_idx=14,
)

clover_world = WorldData(
    borders=[Vec2(75, 625), Vec2(50, 462), Vec2(175, 400), Vec2(50, 337), Vec2(75, 175), Vec2(237, 150), Vec2(300, 275), Vec2(362, 150), Vec2(525, 175), Vec2(550, 337), Vec2(425, 400), Vec2(550, 462), Vec2(525, 625), Vec2(362, 650), Vec2(300, 525), Vec2(237, 650)],
    proyections=[Vec2(273, 482), Vec2(270, 462), Vec2(285, 455), Vec2(270, 447), Vec2(273, 428), Vec2(292, 425), Vec2(300, 440), Vec2(307, 425), Vec2(327, 428), Vec2(330, 447), Vec2(315, 455), Vec2(330, 462), Vec2(327, 482), Vec2(307, 485), Vec2(300, 470), Vec2(292, 485)],
    y3d=55,
    is_loop=True,
    start_idx=13,
)

vee_world = WorldData(
    borders=[Vec2(540, 140), Vec2(510, 205), Vec2(480, 270), Vec2(450, 335), Vec2(420, 400), Vec2(390, 465), Vec2(360, 530), Vec2(330, 595), Vec2(270, 595), Vec2(240, 530), Vec2(210, 465), Vec2(180, 400), Vec2(150, 335), Vec2(120, 270), Vec2(90, 205), Vec2(60, 140)],
    proyections=[Vec2(328, 278), Vec2(325, 286), Vec2(321, 294), Vec2(318, 302), Vec2(314, 310), Vec2(310, 317), Vec2(307, 325), Vec2(303, 333), Vec2(296, 333), Vec2(292, 325), Vec2(289, 317), Vec2(285, 310), Vec2(282, 302), Vec2(278, 294), Vec2(274, 286), Vec2(271, 278)],
    y3d=-90,
    is_loop=False,
    start_idx=8,
)

steps_world = WorldData(
    borders=[Vec2(580, 265), Vec2(580, 355), Vec2(500, 355), Vec2(500, 445), Vec2(420, 445), Vec2(420, 535), Vec2(340, 535), Vec2(340, 625), Vec2(260, 625), Vec2(260, 535), Vec2(180, 535), Vec2(180, 445), Vec2(100, 445), Vec2(100, 355), Vec2(20, 355), Vec2(20, 265)],
    proyections=[Vec2(333, 183), Vec2(333, 194), Vec2(324, 194), Vec2(324, 205), Vec2(314, 205), Vec2(314, 216), Vec2(304, 216), Vec2(304, 227), Vec2(295, 227), Vec2(295, 216), Vec2(285, 216), Vec2(285, 205), Vec2(276, 205), Vec2(276, 194), Vec2(266, 194), Vec2(266, 183)],
    y3d=-200,
    is_loop=False,
    start_idx=8,
)

u_shape_world = WorldData(
    borders=[Vec2(545, 175), Vec2(545, 265), Vec2(545, 355), Vec2(545, 445), Vec2(538, 535), Vec2(492, 625), Vec2(422, 692), Vec2(335, 715), Vec2(265, 715), Vec2(177, 692), Vec2(107, 625), Vec2(62, 535), Vec2(55, 445), Vec2(55, 355), Vec2(55, 265), Vec2(55, 175)],
    proyections=[Vec2(329, 523), Vec2(329, 533), Vec2(329, 544), Vec2(329, 555), Vec2(328, 566), Vec2(323, 577), Vec2(314, 585), Vec2(304, 587), Vec2(295, 587), Vec2(285, 585), Vec2(276, 577), Vec2(271, 566), Vec2(270, 555), Vec2(270, 544), Vec2(270, 533), Vec2(270, 523)],
    y3d=150,
    is_loop=False,
    start_idx=8,
)

line_world = WorldData(
    borders=[Vec2(592, 560), Vec2(553, 560), Vec2(514, 560), Vec2(475, 560), Vec2(436, 560), Vec2(397, 560), Vec2(358, 560), Vec2(319, 560), Vec2(280, 560), Vec2(241, 560), Vec2(202, 560), Vec2(163, 560), Vec2(124, 560), Vec2(85, 560), Vec2(46, 560), Vec2(7, 560)],
    proyections=[Vec2(335, 249), Vec2(330, 249), Vec2(325, 249), Vec2(321, 249), Vec2(316, 249), Vec2(311, 249), Vec2(306, 249), Vec2(302, 249), Vec2(297, 249), Vec2(292, 249), Vec2(288, 249), Vec2(283, 249), Vec2(278, 249), Vec2(274, 249), Vec2(269, 249), Vec2(264, 249)],
    y3d=-170,
    is_loop=False,
    start_idx=8,
)

heart_world = WorldData(
    borders=[Vec2(380, 190), Vec2(500, 200), Vec2(540, 330), Vec2(540, 470), Vec2(500, 575), Vec2(420, 645), Vec2(300, 680), Vec2(180, 645), Vec2(100, 575), Vec2(60, 470), Vec2(60, 330), Vec2(100, 200), Vec2(220, 190), Vec2(280, 295), Vec2(300, 435), Vec2(320, 295)],
    proyections=[Vec2(309, 589), Vec2(324, 591), Vec2(328, 606), Vec2(328, 623), Vec2(324, 636), Vec2(314, 644), Vec2(300, 648), Vec2(285, 644), Vec2(276, 636), Vec2(271, 623), Vec2(271, 606), Vec2(276, 591), Vec2(290, 589), Vec2(297, 602), Vec2(300, 619), Vec2(302, 602)],
    y3d=215,
    is_loop=True,
    start_idx=6,
)

star_world = WorldData(
    borders=[Vec2(165, 543), Vec2(75, 510), Vec2(120, 400), Vec2(75, 290), Vec2(165, 257), Vec2(210, 157), Vec2(300, 213), Vec2(390, 157), Vec2(435, 257), Vec2(525, 290), Vec2(480, 400), Vec2(525, 510), Vec2(435, 543), Vec2(390, 642), Vec2(300, 587), Vec2(210, 642)],
    proyections=[Vec2(283, 477), Vec2(273, 473), Vec2(278, 460), Vec2(273, 446), Vec2(283, 442), Vec2(289, 430), Vec2(300, 437), Vec2(310, 430), Vec2(316, 442), Vec2(327, 446), Vec2(321, 460), Vec2(327, 473), Vec2(316, 477), Vec2(310, 489), Vec2(300, 482), Vec2(289, 489)],
    y3d=60,
    is_loop=True,
    start_idx=14,
)

w_shape_world = WorldData(
    borders=[Vec2(580, 295), Vec2(545, 365), Vec2(534, 452), Vec2(513, 529), Vec2(464, 582), Vec2(394, 582), Vec2(352, 540), Vec2(321, 470), Vec2(279, 470), Vec2(247, 540), Vec2(205, 582), Vec2(135, 582), Vec2(86, 529), Vec2(65, 452), Vec2(55, 365), Vec2(20, 295)],
    proyections=[Vec2(333, 217), Vec2(329, 225), Vec2(328, 236), Vec2(325, 245), Vec2(319, 251), Vec2(311, 251), Vec2(306, 246), Vec2(302, 238), Vec2(297, 238), Vec2(293, 246), Vec2(288, 251), Vec2(280, 251), Vec2(274, 245), Vec2(271, 236), Vec2(270, 225), Vec2(266, 217)],
    y3d=-170,
    is_loop=False,
    start_idx=8,
)

broken_v_world = WorldData(
    borders=[Vec2(580, 120), Vec2(562, 211), Vec2(545, 295), Vec2(527, 393), Vec2(440, 375), Vec2(398, 452), Vec2(373, 540), Vec2(338, 592), Vec2(265, 575), Vec2(212, 627), Vec2(170, 540), Vec2(142, 470), Vec2(125, 365), Vec2(107, 295), Vec2(72, 225), Vec2(20, 155)],
    proyections=[Vec2(333, 276), Vec2(331, 287), Vec2(329, 297), Vec2(327, 309), Vec2(316, 307), Vec2(311, 316), Vec2(308, 326), Vec2(304, 333), Vec2(295, 331), Vec2(289, 337), Vec2(284, 326), Vec2(281, 318), Vec2(279, 305), Vec2(276, 297), Vec2(272, 289), Vec2(266, 280)],
    y3d=-90,
    is_loop=False,
    start_idx=8,
)

infinity_world = WorldData(
    borders=[Vec2(300, 400), Vec2(348, 290), Vec2(444, 235), Vec2(540, 290), Vec2(588, 400), Vec2(540, 510), Vec2(444, 565), Vec2(348, 510), Vec2(300, 400), Vec2(252, 290), Vec2(156, 235), Vec2(60, 290), Vec2(12, 400), Vec2(60, 510), Vec2(156, 565), Vec2(252, 510)],
    proyections=[Vec2(300, 400), Vec2(305, 386), Vec2(317, 380), Vec2(328, 386), Vec2(334, 400), Vec2(328, 413), Vec2(317, 419), Vec2(305, 413), Vec2(300, 400), Vec2(294, 386), Vec2(282, 380), Vec2(271, 386), Vec2(265, 400), Vec2(271, 413), Vec2(282, 419), Vec2(294, 413)],
    y3d=0,
    is_loop=True,
    start_idx=1,
)
