from pyray import Vector2
import math


SCREEN_WIDTH: int = 600
SCREEN_HEIGHT: int = 800
screen_center = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)


def circle():
    radius_px = 250
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
        x = int(-stepsx[a] * 125) + screen_center.x
        y = int(stepsy[a] * 125) + screen_center.y
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
        x = int(-stepsx[a] * 125) + screen_center.x
        y = int(stepsy[a] * 125) + screen_center.y
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
        x = int(-stepsx[a] * 40) + screen_center.x
        y = int(-stepsy[a] * 40) + screen_center.y
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
        x = int(-stepsx[a] * 40) + screen_center.x
        y = int(stepsy[a] * 33) + screen_center.y
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
        x = int(-stepsx[a] * 125) + screen_center.x
        y = int(stepsy[a] * 125) + screen_center.y
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
        y = int(-stepsy[a] * 65) + screen_center.y
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
        y = int(stepsy[a] * 45) + screen_center.y
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
        x = int(stepsx[a] * 35) + screen_center.x
        y = int(stepsy[a] * 45) + screen_center.y
        xs.append(x)
        ys.append(y)
    print(xs)
    print(ys)

def line():
    xp = -7.5
    xs = []
    ys = []
    for _ in range(16):
        x = int(-xp*39) + screen_center.x
        y = 160 + screen_center.y
        xp+=1
        xs.append(x)
        ys.append(y)
    print(xs)
    print(ys)

def heart():
    stepsx = [2.0, 5.0, 6.0, 6.0, 5.0, 3.0, 0.0,-3.0,-5.0,-6.0,-6.0,-5.0,-2.0,-0.5, 0.0, 0.5]
    stepsy = [6.0, 5.7, 2.0,-2.0,-5.0,-7.0,-8.0,-7.0,-5.0,-2.0, 2.0, 5.7, 6.0, 3.0,-1.0, 3.0]
    
    xs = []
    ys = []
    for a in range(16):
        x = int(stepsx[a]*40) + screen_center.x
        y = int(-stepsy[a]*35) + screen_center.y
        xs.append(x)
        ys.append(y)
    print(xs)
    print(ys)

def star():
    stepsx = [1.5,2.5,2.0, 2.5, 1.5, 1.0, 0.0,-1.0,-1.5,-2.5,-2.0,-2.5,-1.5,-1.0,0.0,1.0]
    stepsy = [1.3,1.0,0.0,-1.0,-1.3,-2.2,-1.7,-2.2,-1.3,-1.0, 0.0, 1.0, 1.3, 2.2,1.7,2.2]

    xs = []
    ys = []
    for a in range(16):
        x = int(-stepsx[a]*90) + screen_center.x
        y = int(stepsy[a]*110) + screen_center.y
        xs.append(x)
        ys.append(y)
    print(xs)
    print(ys)

def w_shape():
    stepsx = [ 8.0, 7.0, 6.7, 6.1, 4.7, 2.7, 1.5, 0.6,-0.6,-1.5,-2.7,-4.7,-6.1,-6.7,-7.0,-8.0]
    stepsy = [-3.0,-1.0, 1.5, 3.7, 5.2, 5.2, 4.0, 2.0, 2.0, 4.0, 5.2, 5.2, 3.7, 1.5,-1.0,-3.0]

    xs = []
    ys = []
    for a in range(16):
        x = int(stepsx[a]*35) + screen_center.x
        y = int(stepsy[a]*35) + screen_center.y
        xs.append(x)
        ys.append(y)
    print(xs)
    print(ys)


def broken_v():
    stepsx = [ -8.0, -7.5, -7.0, -6.5, -4.0, -2.8, -2.1, -1.1, 1.0, 2.5, 3.7, 4.5, 5.0, 5.5, 6.5,8.0]
    stepsy = [ 8.0, 5.4, 3.0, 0.2, 0.7,-1.5,-4.0,-5.5,-5.0,-6.5,-4.0,-2.0, 1.0, 3.0, 5.0, 7.0]

    xs = []
    ys = []
    for a in range(16):
        x = int(-stepsx[a]*35) + screen_center.x
        y = int(-stepsy[a]*35) + screen_center.y
        xs.append(x)
        ys.append(y)
    print(xs)
    print(ys)

def infinity():
    stepsx = [0.0,-1.0,-3.0,-5.0,-6.0,-5.0,-3.0,-1.0, 0.0, 1.0, 3.0, 5.0, 6.0, 5.0, 3.0, 1.0]
    stepsy = [0.0, 2.0, 3.0, 2.0, 0.0,-2.0,-3.0,-2.0, 0.0, 2.0, 3.0, 2.0, 0.0,-2.0,-3.0,-2.0]

    xs = []
    ys = []
    for a in range(16):
        x = int(-stepsx[a]*48) + screen_center.x
        y = int(-stepsy[a]*55) + screen_center.y
        xs.append(x)
        ys.append(y)
    print(xs)
    print(ys)



def main():
    # circle()
    # square()
    # plus()
    # peanut()
    # cross()
    # triangle()
    # clover()
    # vee()
    steps()
    # u_shape()
    # line()
    # heart()
    # star()
    # w_shape()
    # broken_v()
    # infinity()
    pass


if __name__ == "__main__":
    main()
