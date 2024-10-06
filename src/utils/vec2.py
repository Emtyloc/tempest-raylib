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
            res = vector_2divide(self, other)
            return self.to_Vec2(res)
        return Vec2(self.x / other, self.y / other)
    
    def __itruediv__(self, other):
        if isinstance(other, Vec2):
            res = vector_2divide(self, other)
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
        return vector_2distance(self, vec2)
    
    def distance_sqr(self, vec2) -> float:
        return vector_2distance_sqr(self, vec2)
    
    def dot_product(self, vec2) -> float:
        return vector_2dot_product(self, vec2)
    
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
    
    # Project custom functions
    
    def center_scale(self, center, scale_factor: float):
        """
        Scale vector using center reference(vector) by scale factor.
        """
        offset_vector = vector2_subtract(self, center)
        scaled_offset = vector2_scale(offset_vector, scale_factor) 
        scaled_vector = vector2_add(center, scaled_offset)
        return self.to_Vec2(scaled_vector)

    def perp_norm(self):
        """
        Returns normalize perpendicular vector.
        """
        return self.to_Vec2(vector2_normalize(Vector2(-self.y, self.x)))