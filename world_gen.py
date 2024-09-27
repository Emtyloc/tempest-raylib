from pyray import Vector2
import math


SCREEN_WIDTH: int = 600
SCREEN_HEIGHT: int = 800
screen_center = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)


def circle():
    radius_px = 200
    center = screen_center

    xs = []
    ys = []
    for i in range(16):
        x = int(math.cos(math.radians(i * 22.5)) * radius_px) + center.x
        y = int(math.sin(math.radians(i * 22.5)) * radius_px) + center.y
        xs.append(x)
        ys.append(y)
    print(xs)
    print(ys)

def square():
    stepsx = [2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 0.0, -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0, 0.0, 1.0]
    stepsy = [2.0, 1.0, 0.0, -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0, 0.0, 1.0, 2.0, 2.0, 2.0, 2.0]

    xs = []
    ys = []
    for a in range(16):
        x = int(-stepsx[a] * 100) + screen_center.x
        y = int(stepsy[a] * 100) + screen_center.y
        xs.append(x)
        ys.append(y)
    print(xs)
    print(ys)

def plus():
    stepsx = [1.0, 2.0, 2.0, 2.0, 1.0, 1.0, 0.0, -1.0, -1.0, -2.0, -2.0, -2.0, -1.0, -1.0, 0.0, 1.0]
    stepsy = [1.0, 1.0, 0.0, -1.0, -1.0, -2.0, -2.0, -2.0, -1.0, -1.0, 0.0, 1.0, 1.0, 2.0, 2.0, 2.0]

    xs = []
    ys = []
    for a in range(16):
        x = int(-stepsx[a] * 100) + screen_center.x
        y = int(stepsy[a] * 100) + screen_center.y
        xs.append(x)
        ys.append(y)
    print(xs)
    print(ys)

def peanut():
    stepsx = [1.0, 3.0, 5.5, 6.5, 6.5, 5.5, 3.0, 1.0, -1.0, -3.0, -5.5, -6.5, -6.5, -5.5, -3.0, -1.0]
    stepsy = [-3.5, -5.0, -4.0, -2.0, 1.0, 3.0, 4.0, 2.5, 2.5, 4.0, 3.0, 1.0, -2.0, -4.0, -5.0, -3.5]

    xs = []
    ys = []
    for a in range(16):
        x = int(-stepsx[a] * 40) + screen_center.x
        y = int(-stepsy[a] * 30) + screen_center.y - 15
        xs.append(x)
        ys.append(y)
    print(xs)
    print(ys)


def cross():
    stepsx = [1.0, 2.0, 4.0, 7.0, 7.0, 4.0, 2.0, 1.0, -1.0, -2.0, -4.0, -7.0, -7.0, -4.0, -2.0, -1.0]
    stepsy = [-7.0, -4.0, -2.0, -1.0, 1.0, 2.0, 4.0, 7.0, 7.0, 4.0, 2.0, 1.0, -1.0, -2.0, -4.0, -7.0]

    xs = []
    ys = []
    for a in range(16):
        x = int(-stepsx[a] * 30) + screen_center.x
        y = int(-stepsy[a] * 30) + screen_center.y
        xs.append(x)
        ys.append(y)
    print(xs)
    print(ys)

def triangle():
    stepsx = [3.4, 5.0, 4.0, 3.0, 2.0, 1.0, 0.0, -1.0, -2.0, -3.0, -4.0, -5.0, -3.4, -1.6, 0.0, 1.6]
    stepsy = [6.0, 6.0, 3.0, 0.0, -3.0, -6.0, -9.0, -6.0, -3.0, 0.0, 3.0, 6.0, 6.0, 6.0, 6.0, 6.0]

    xs = []
    ys = []
    for a in range(16):
        x = int(-stepsx[a] * 35) + screen_center.x
        y = int(stepsy[a] * 28) + screen_center.y
        xs.append(x)
        ys.append(y)
    print(xs)
    print(ys)

def clover():
    stepsx = [1.8, 2.0, 1.0, 2.0, 1.8, 0.5, 0.0, -0.5, -1.8, -2.0, -1.0, -2.0, -1.8, -0.5, 0.0, 0.5]
    stepsy = [1.8, 0.5, 0.0, -0.5, -1.8, -2.0, -1.0, -2.0, -1.8, -0.5, 0.0, 0.5, 1.8, 2.0, 1.0, 2.0]

    xs = []
    ys = []
    for a in range(16):
        x = int(-stepsx[a] * 100) + screen_center.x
        y = int(stepsy[a] * 100) + screen_center.y
        xs.append(x)
        ys.append(y)
    print(xs)
    print(ys)

def vee():
    stepsx = [8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0, -1.0, -2.0, -3.0, -4.0, -5.0, -6.0, -7.0, -8.0]
    stepsy = [4.0, 3.0, 2.0, 1.0, 0.0, -1.0, -2.0, -3.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0]

    xs = []
    ys = []
    for a in range(16):
        x = int(stepsx[a] * 30) + screen_center.x
        y = int(-stepsy[a] * 55) + screen_center.y
        xs.append(x)
        ys.append(y)
    print(xs)
    print(ys)

def steps():
    stepsx = [7.0, 7.0, 5.0, 5.0, 3.0, 3.0, 1.0, 1.0, -1.0, -1.0, -3.0, -3.0, -5.0, -5.0, -7.0, -7.0]
    stepsy = [-3.0, -1.0, -1.0, 1.0, 1.0, 3.0, 3.0, 5.0, 5.0, 3.0, 3.0, 1.0, 1.0, -1.0, -1.0, -3.0]

    xs = []
    ys = []
    for a in range(16):
        x = int(stepsx[a] * 40) + screen_center.x
        y = int(stepsy[a] * 36) + screen_center.y
        xs.append(x)
        ys.append(y)
    print(xs)
    print(ys)

def u_shape():
    stepsx = [7.0, 7.0, 7.0, 7.0, 6.8, 5.5, 3.5, 1.0, -1.0, -3.5, -5.5, -6.8, -7.0, -7.0, -7.0, -7.0]
    stepsy = [-5.0, -3.0, -1.0, 1.0, 3.0, 5.0, 6.5, 7.0, 7.0, 6.5, 5.0, 3.0, 1.0, -1.0, -3.0, -5.0]

    xs = []
    ys = []
    for a in range(16):
        x = int(stepsx[a] * 30) + screen_center.x
        y = int(stepsy[a] * 35) + screen_center.y
        xs.append(x)
        ys.append(y)
    print(xs)
    print(ys)



def main():
    # circle_hole()
    # square()
    # cross()
    # peanut()
    # cross()
    # triangle()
    # clover()
    vee()
    steps()
    u_shape()



if __name__ == "__main__":
    main()
