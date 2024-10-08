import math
from src.utils import Vec2
from src.shared import SCREEN_CENTER



def get_proyections(borders: list[Vec2], y3d: float) -> list[Vec2]:
    """
    Compute and get the proyection of the level using x,y coordenates and the y3d offset.
    """
    PROYECTION_SCALE = 0.12
    
    proyections: list[Vec2] = []
    for border in borders:
        center_scaled = border.center_scale(SCREEN_CENTER, PROYECTION_SCALE)
        proyection_vec = Vec2(int(center_scaled.x), int(center_scaled.y + y3d))
        proyections.append(proyection_vec)
    
    return proyections

def circle():
    radius_px = 250
    center = SCREEN_CENTER
    y3d=80

    borders = []
    for i in range(16):
        x = int(math.cos(math.radians(i * 22.5)) * radius_px + center.x)
        y = int(math.sin(math.radians(i * 22.5)) * radius_px + center.y)
        borders.append(Vec2(x, y))
    print("circle")
    print("Borders:")
    print([f"Vec2({border})" for border in borders])
    print("Proyections:")
    print([f"Vec2({proy})" for proy in get_proyections(borders, y3d)])




def square():
    stepsx = [2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 0.0, -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0, 0.0, 1.0]
    stepsy = [2.0, 1.0, 0.0, -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0, 0.0, 1.0, 2.0, 2.0, 2.0, 2.0]
    y3d=80

    borders = []
    for a in range(16):
        x = int(-stepsx[a] * 125 + SCREEN_CENTER.x)
        y = int(stepsy[a] * 125 + SCREEN_CENTER.y)
        borders.append(Vec2(x, y))
    print("square")
    print("Borders:")
    print([f"Vec2({border})" for border in borders])
    print("Proyections:")
    print([f"Vec2({proy})" for proy in get_proyections(borders, y3d)])

def plus():
    stepsx = [1.0, 2.0, 2.0, 2.0, 1.0, 1.0, 0.0, -1.0, -1.0, -2.0, -2.0, -2.0, -1.0, -1.0, 0.0, 1.0]
    stepsy = [1.0, 1.0, 0.0, -1.0, -1.0, -2.0, -2.0, -2.0, -1.0, -1.0, 0.0, 1.0, 1.0, 2.0, 2.0, 2.0]
    y3d=70

    borders = []
    for a in range(16):
        x = int(-stepsx[a] * 125 + SCREEN_CENTER.x)
        y = int(stepsy[a] * 125 + SCREEN_CENTER.y)
        borders.append(Vec2(x, y))
    print("plus")
    print("Borders:")
    print([f"Vec2({border})" for border in borders])
    print("Proyections:")
    print([f"Vec2({proy})" for proy in get_proyections(borders, y3d)])

def peanut():
    stepsx = [1.0, 3.0, 5.5, 6.5, 6.5, 5.5, 3.0, 1.0, -1.0, -3.0, -5.5, -6.5, -6.5, -5.5, -3.0, -1.0]
    stepsy = [-3.5, -5.0, -4.0, -2.0, 1.0, 3.0, 4.0, 2.5, 2.5, 4.0, 3.0, 1.0, -2.0, -4.0, -5.0, -3.5]
    y3d=45

    borders = []
    for a in range(16):
        x = int(-stepsx[a] * 40 + SCREEN_CENTER.x)
        y = int(-stepsy[a] * 30 + SCREEN_CENTER.y - 15)
        borders.append(Vec2(x, y))
    print("peanut")
    print("Borders:")
    print([f"Vec2({border})" for border in borders])
    print("Proyections:")
    print([f"Vec2({proy})" for proy in get_proyections(borders, y3d)])


def cross():
    stepsx = [1.0, 2.0, 4.0, 7.0, 7.0, 4.0, 2.0, 1.0, -1.0, -2.0, -4.0, -7.0, -7.0, -4.0, -2.0, -1.0]
    stepsy = [-7.0, -4.0, -2.0, -1.0, 1.0, 2.0, 4.0, 7.0, 7.0, 4.0, 2.0, 1.0, -1.0, -2.0, -4.0, -7.0]
    y3d=70

    borders = []
    for a in range(16):
        y = int(-stepsy[a] * 40 + SCREEN_CENTER.y)
        x = int(-stepsx[a] * 40 + SCREEN_CENTER.x)
        borders.append(Vec2(x, y))
    print("cross")
    print("Borders:")
    print([f"Vec2({border})" for border in borders])
    print("Proyections:")
    print([f"Vec2({proy})" for proy in get_proyections(borders, y3d)])

def triangle():
    stepsx = [3.4, 5.0, 4.0, 3.0, 2.0, 1.0, 0.0, -1.0, -2.0, -3.0, -4.0, -5.0, -3.4, -1.6, 0.0, 1.6]
    stepsy = [6.0, 6.0, 3.0, 0.0, -3.0, -6.0, -9.0, -6.0, -3.0, 0.0, 3.0, 6.0, 6.0, 6.0, 6.0, 6.0]
    y3d=40

    borders = []
    for a in range(16):
        x = int(-stepsx[a] * 40 + SCREEN_CENTER.x)
        y = int(stepsy[a] * 33 + SCREEN_CENTER.y)
        borders.append(Vec2(x, y))
    print("triangle")
    print("Borders:")
    print([f"Vec2({border})" for border in borders])
    print("Proyections:")
    print([f"Vec2({proy})" for proy in get_proyections(borders, y3d)])

def clover():
    stepsx = [1.8, 2.0, 1.0, 2.0, 1.8, 0.5, 0.0, -0.5, -1.8, -2.0, -1.0, -2.0, -1.8, -0.5, 0.0, 0.5]
    stepsy = [1.8, 0.5, 0.0, -0.5, -1.8, -2.0, -1.0, -2.0, -1.8, -0.5, 0.0, 0.5, 1.8, 2.0, 1.0, 2.0]
    y3d=55

    borders = []
    for a in range(16):
        x = int(-stepsx[a] * 125 + SCREEN_CENTER.x)
        y = int(stepsy[a] * 125 + SCREEN_CENTER.y)
        borders.append(Vec2(x, y))
    print("clover")
    print("Borders:")
    print([f"Vec2({border})" for border in borders])
    print("Proyections:")
    print([f"Vec2({proy})" for proy in get_proyections(borders, y3d)])

def vee():
    stepsx = [8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0, -1.0, -2.0, -3.0, -4.0, -5.0, -6.0, -7.0, -8.0]
    stepsy = [4.0, 3.0, 2.0, 1.0, 0.0, -1.0, -2.0, -3.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0]
    y3d=-90

    borders = []
    for a in range(16):
        x = int(stepsx[a] * 30 + SCREEN_CENTER.x)
        y = int(-stepsy[a] * 65 + SCREEN_CENTER.y)
        borders.append(Vec2(x, y))
    print("vee")
    print("Borders:")
    print([f"Vec2({border})" for border in borders])
    print("Proyections:")
    print([f"Vec2({proy})" for proy in get_proyections(borders, y3d)])

def steps():
    stepsx = [7.0, 7.0, 5.0, 5.0, 3.0, 3.0, 1.0, 1.0, -1.0, -1.0, -3.0, -3.0, -5.0, -5.0, -7.0, -7.0]
    stepsy = [-3.0, -1.0, -1.0, 1.0, 1.0, 3.0, 3.0, 5.0, 5.0, 3.0, 3.0, 1.0, 1.0, -1.0, -1.0, -3.0]
    y3d=-200

    borders = []
    for a in range(16):
        x = int(stepsx[a] * 40 + SCREEN_CENTER.x)
        y = int(stepsy[a] * 45 + SCREEN_CENTER.y)
        borders.append(Vec2(x, y))
    print("steps")
    print("Borders:")
    print([f"Vec2({border})" for border in borders])
    print("Proyections:")
    print([f"Vec2({proy})" for proy in get_proyections(borders, y3d)])

def u_shape():
    stepsx = [7.0, 7.0, 7.0, 7.0, 6.8, 5.5, 3.5, 1.0, -1.0, -3.5, -5.5, -6.8, -7.0, -7.0, -7.0, -7.0]
    stepsy = [-5.0, -3.0, -1.0, 1.0, 3.0, 5.0, 6.5, 7.0, 7.0, 6.5, 5.0, 3.0, 1.0, -1.0, -3.0, -5.0]
    y3d=150

    borders = []
    for a in range(16):
        x = int(stepsx[a] * 35 + SCREEN_CENTER.x)
        y = int(stepsy[a] * 45 + SCREEN_CENTER.y)
        borders.append(Vec2(x, y))
    print("u_shape")
    print("Borders:")
    print([f"Vec2({border})" for border in borders])
    print("Proyections:")
    print([f"Vec2({proy})" for proy in get_proyections(borders, y3d)])

def line():
    xp = -7.5
    y3d=-170
    
    borders = []
    for _ in range(16):
        x = int(-xp*39 + SCREEN_CENTER.x)
        y = int(160 + SCREEN_CENTER.y)
        xp+=1
        borders.append(Vec2(x, y))
    print("line")
    print("Borders:")
    print([f"Vec2({border})" for border in borders])
    print("Proyections:")
    print([f"Vec2({proy})" for proy in get_proyections(borders, y3d)])

def heart():
    stepsx = [2.0, 5.0, 6.0, 6.0, 5.0, 3.0, 0.0,-3.0,-5.0,-6.0,-6.0,-5.0,-2.0,-0.5, 0.0, 0.5]
    stepsy = [6.0, 5.7, 2.0,-2.0,-5.0,-7.0,-8.0,-7.0,-5.0,-2.0, 2.0, 5.7, 6.0, 3.0,-1.0, 3.0]
    y3d=215

    borders = []
    for a in range(16):
        x = int(stepsx[a]*40 + SCREEN_CENTER.x)
        y = int(-stepsy[a]*35 + SCREEN_CENTER.y)
        borders.append(Vec2(x, y))
    print("heart")
    print("Borders:")
    print([f"Vec2({border})" for border in borders])
    print("Proyections:")
    print([f"Vec2({proy})" for proy in get_proyections(borders, y3d)])

def star():
    stepsx = [1.5,2.5,2.0, 2.5, 1.5, 1.0, 0.0,-1.0,-1.5,-2.5,-2.0,-2.5,-1.5,-1.0,0.0,1.0]
    stepsy = [1.3,1.0,0.0,-1.0,-1.3,-2.2,-1.7,-2.2,-1.3,-1.0, 0.0, 1.0, 1.3, 2.2,1.7,2.2]
    y3d=60

    borders = []
    for a in range(16):
        x = int(-stepsx[a]*90 + SCREEN_CENTER.x)
        y = int(stepsy[a]*110 + SCREEN_CENTER.y)
        borders.append(Vec2(x, y))
    print("star")
    print("Borders:")
    print([f"Vec2({border})" for border in borders])
    print("Proyections:")
    print([f"Vec2({proy})" for proy in get_proyections(borders, y3d)])

def w_shape():
    stepsx = [ 8.0, 7.0, 6.7, 6.1, 4.7, 2.7, 1.5, 0.6,-0.6,-1.5,-2.7,-4.7,-6.1,-6.7,-7.0,-8.0]
    stepsy = [-3.0,-1.0, 1.5, 3.7, 5.2, 5.2, 4.0, 2.0, 2.0, 4.0, 5.2, 5.2, 3.7, 1.5,-1.0,-3.0]
    y3d=-170
    
    borders = []
    for a in range(16):
        x = int(stepsx[a]*35 + SCREEN_CENTER.x)
        y = int(stepsy[a]*35 + SCREEN_CENTER.y)
        borders.append(Vec2(x, y))
    print("w_shape")
    print("Borders:")
    print([f"Vec2({border})" for border in borders])
    print("Proyections:")
    print([f"Vec2({proy})" for proy in get_proyections(borders, y3d)])


def broken_v():
    stepsx = [ -8.0, -7.5, -7.0, -6.5, -4.0, -2.8, -2.1, -1.1, 1.0, 2.5, 3.7, 4.5, 5.0, 5.5, 6.5,8.0]
    stepsy = [ 8.0, 5.4, 3.0, 0.2, 0.7,-1.5,-4.0,-5.5,-5.0,-6.5,-4.0,-2.0, 1.0, 3.0, 5.0, 7.0]
    y3d=-90

    borders = []
    for a in range(16):
        x = int(-stepsx[a]*35 + SCREEN_CENTER.x)
        y = int(-stepsy[a]*35 + SCREEN_CENTER.y)
        borders.append(Vec2(x, y))
    print("broken_v")
    print("Borders:")
    print([f"Vec2({border})" for border in borders])
    print("Proyections:")
    print([f"Vec2({proy})" for proy in get_proyections(borders, y3d)])

def infinity():
    stepsx = [0.0,-1.0,-3.0,-5.0,-6.0,-5.0,-3.0,-1.0, 0.0, 1.0, 3.0, 5.0, 6.0, 5.0, 3.0, 1.0]
    stepsy = [0.0, 2.0, 3.0, 2.0, 0.0,-2.0,-3.0,-2.0, 0.0, 2.0, 3.0, 2.0, 0.0,-2.0,-3.0,-2.0]
    y3d=0

    borders = []
    for a in range(16):
        x = int(-stepsx[a]*48 + SCREEN_CENTER.x)
        y = int(-stepsy[a]*55 + SCREEN_CENTER.y)
        borders.append(Vec2(x, y))
    print("infinity")
    print("Borders:")
    print([f"Vec2({border})" for border in borders])
    print("Proyections:")
    print([f"Vec2({proy})" for proy in get_proyections(borders, y3d)])



def main():
    circle()
    square()
    plus()
    peanut()
    cross()
    triangle()
    clover()
    vee()
    steps()
    u_shape()
    line()
    heart()
    star()
    w_shape()
    broken_v()
    infinity()


if __name__ == "__main__":
    main()
