from pyray import *

class Vec2(list):
    def __init__(self, x, y):
        super(Vec2, self).__init__([x, y])

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, value):
        self[0]= value

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, value):
        self[1]= value
    
    @staticmethod
    def to_Vec2(v: Vector2):
        """
        Cast Vector2 to Vec2.
        """
        return Vec2(v.x, v.y)
    
    def __repr__(self) -> str:
        return f"{self.x}, {self.y}"
    
    def __eq__(self, other):
        if isinstance(other, Vec2):
            return self.x == other.x and self.y == other.y
        return False
    
    def __add__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x + other.x, self.y + other.y)
        return Vec2(self.x + other, self.y + other)
    
    def __iadd__(self, other):
        if isinstance(other, Vec2):
            self.x += other.x
            self.y += other.y
        else:
            res = vector2_add_value(self, other)
            self.x = res.x
            self.y = res.y
        return self
    
    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x - other.x, self.y - other.y)
        return Vec2(self.x - other, self.y - other)
    
    def __isub__(self, other):
        if isinstance(other, Vec2):
            self.x -= other.x
            self.y -= other.y
        else:
            self.x -= other
            self.y -= other
        return self
    
    def __rsub__(self, other):
        return Vec2(other - self.x, other - self.y)
    
    def __mul__(self, other):
        if isinstance(other, Vec2):
            res = vector2_multiply(self, other)
            return self.to_Vec2(res)
        return Vec2(self.x * other, self.y * other)
    
    def __imul__(self, other):
        if isinstance(other, Vec2):
            res = vector2_multiply(self, other)
        else:
            res = vector2_scale(self, other)
        self.x = res.x
        self.y = res.y
        return self
    
    def __truediv__(self, other):
        if isinstance(other, Vec2):
            res = vector2_divide(self, other)
            return self.to_Vec2(res)
        return Vec2(self.x / other, self.y / other)
    
    def __itruediv__(self, other):
        if isinstance(other, Vec2):
            res = vector2_divide(self, other)
        else:
            res = vector2_scale(self, 1/other)
        self.x = res.x
        self.y = res.y
        return self
    
    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __pos__(self):
        return Vec2(self.x, self.y)
    
    def __pow__(self, exponent):
        return Vec2(self.x ** exponent, self.y ** exponent)

    # PyRay mapped vector2 functions
    
    def angle(self, vec2):
        return vector2_angle(self, vec2)
    
    def clamp(self, min_vec2, max_vec2):
        res = vector2_clamp(self, min_vec2, max_vec2)
        return self.to_Vec2(res)
        
    def clamp_value(self, min_val: float, max_val: float):
        res = vector2_clamp_value(self, min_val, max_val)
        return self.to_Vec2(res)
    
    def distance(self, vec2):
        return vector2_distance(self, vec2)
    
    def distance_sqr(self, vec2) -> float:
        return vector2_distance_sqr(self, vec2)
    
    def dot_product(self, vec2) -> float:
        return vector2_dot_product(self, vec2)
    
    def invert(self):
        res = vector2_invert(self)
        return self.to_Vec2(res)

    def length(self):
        return vector2_length(self)

    def length_sqr(self) -> float:
        return vector2_length_sqr(self)
    
    def lerp(self, vec2, amount: float):
        res = vector2_lerp(self, vec2, amount)
        return self.to_Vec2(res)
    
    def move_towards(self, target_vec2, max_distance: float):
        res = vector2_move_towards(self, target_vec2, max_distance)
        return self.to_Vec2(res)

    def negate(self):
        res = vector2_negate(self)
        return self.to_Vec2(res)

    def normalize(self):
        res =  vector2_normalize(self)
        return self.to_Vec2(res)
        
    def reflect(self, normal_vec2):
        res = vector2_reflect(self, normal_vec2)
        return self.to_Vec2(res)

    def rotate(self, angle: float):
        res = vector2_rotate(self, angle)
        return self.to_Vec2(res)

    def transform(self, mat: Matrix):
        res = vector2_transform(self, mat)
        return self.to_Vec2(res)
    
    @staticmethod
    def line_angle(start_vec2, end_vec2) -> float:
        return vector2_line_angle(start_vec2, end_vec2)
    
    @staticmethod
    def one():
        return Vec2(1, 1)
    
    @staticmethod
    def zero():
        return Vec2(0, 0)

    
if __name__ == "__main__":
    # Arithmetic ops
    v1 = Vec2(5, 5)
    v2 = Vec2(10, 10)
    
    print(v1 + v2) # 15, 15
    print(v1 - v2) # -5, -5

    print(v1 * v2) # 50.0, 50.0
    print(v1 / v2) # 0.5, 0.5

    print(v1 * 2) # 10, 10
    print(v2 / 2) # 5.0, 5.0

    v1+=v2
    print(v1) #15, 15
    v2-=v1
    print(v2) #-5, -5

    v1/=-v2
    print(v1) #3.0, 3.0
    v2*=v1
    print(v2) #-15.0, -15.0

    v3 = Vec2(3, 5)
    print(v3 ** 2) #9, 25

    v1 = Vec2.one()
    print(v1)

    v0 = Vec2.zero()
    print(v0)

    # Vector2 pyray methods
    v1 = Vec2(3, 4)
    v2 = Vec2(1, 2)
    v_min = Vec2(0, 0)
    v_max = Vec2(5, 5)
    
    print("Angle:", v1.angle(v2))
    
    print("Clamp:", v1.clamp(v_min, v_max))
    
    print("Clamp value:", v1.clamp_value(1.5, 3.5))
    
    print("Distance:", v1.distance(v2))
    
    print("Distance Sqr:", v1.distance_sqr(v2))
    
    print("Dot Product:", v1.dot_product(v2))
    
    print("Invert:", v1.invert())
    
    print("Length:", v1.length())
    
    print("Length Sqr:", v1.length_sqr())
    
    print("Lerp:", v1.lerp(v2, 0.5))
    
    print("Line Angle:", Vec2.line_angle(v1, v2))
    
    print("Move Towards:", v1.move_towards(v2, 0.5))
    
    print("Negate:", v1.negate())
    
    print("Normalize:", v1.normalize())
    
    print("Reflect:", v1.reflect(v2))
    
    print("Rotate:", v1.rotate(45))
    
    # I don't know why this not work
    # mat = Matrix2x2(1, 0, 0, 1)
    # print("Transform:", v1.transform(mat))
    