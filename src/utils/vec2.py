from pyray import *


class Vec2:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    @property
    def vector2(self):
        """
        Cast Vec2 to Vector2.
        """
        return Vector2(self.x, self.y)
    
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
            res = vector2_multiply(self.vector2, other.vector2)
            return self.to_Vec2(res)
        return Vec2(self.x * other, self.y * other)
    
    def __imul__(self, other):
        if isinstance(other, Vec2):
            res = vector2_multiply(self.vector2, other.vector2)
        else:
            res = vector2_scale(self.vector2, other)
        self.x = res.x
        self.y = res.y
        return self
    
    def __truediv__(self, other):
        if isinstance(other, Vec2):
            res = vector_2divide(self.vector2, other.vector2)
            return self.to_Vec2(res)
        return Vec2(self.x / other, self.y / other)
    
    def __itruediv__(self, other):
        if isinstance(other, Vec2):
            res = vector_2divide(self.vector2, other.vector2)
        else:
            res = vector2_scale(self.vector2, 1/other)
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
    
    def angle(self, other):
        return vector2_angle(self.vector2, other.vector2)
    
    def clamp(self, min_vec2, max_vec2):
        res = vector2_clamp(self.vector2, min_vec2.vector2, max_vec2.vector2)
        return self.to_Vec2(res)
        
    def clamp_value(self, min_val: float, max_val: float):
        res = vector2_clamp_value(self.vector2, min_val, max_val)
        return self.to_Vec2(res)
    
    def distance(self, v):
        return vector_2distance(self.vector2, v.vector2)
    
    def distance_sqr(self, v) -> float:
        return vector_2distance_sqr(self.vector2, v.vector2)
    
    def dot_product(self, v) -> float:
        return vector_2dot_product(self.vector2, v.vector2)
    
    def invert(self):
        res = vector2_invert(self.vector2)
        return self.to_Vec2(res)

    def length(self):
        return vector2_length(self.vector2)

    def length_sqr(self) -> float:
        return vector2_length_sqr(self.vector2)
    
    def lerp(self, v, amount: float):
        res = vector2_lerp(self.vector2, v.vector2, amount)
        return self.to_Vec2(res)
    
    def move_towards(self, target_v, max_distance: float):
        res = vector2_move_towards(self.vector2, target_v.vector2, max_distance)
        return self.to_Vec2(res)

    def vector2_negate(self):
        res = vector2_negate(self.vector2)
        return self.to_Vec2(res)

    def vector2_normalize(self):
        res =  vector2_normalize(self.vector2)
        return self.to_Vec2(res)
        
    def vector2_reflect(self, normal_v):
        res = vector2_reflect(self.vector2, normal_v.vector2)
        return self.to_Vec2(res)

    def vector2_rotate(self, angle: float):
        res = vector2_rotate(self.vector2, angle)
        return self.to_Vec2(res)

    def transform(self, mat: Matrix):
        res = vector2_transform(self.vector2, mat)
        return self.to_Vec2(res)
    
    @staticmethod
    def line_angle(start_v, end_v) -> float:
        return vector2_line_angle(start_v.vector2, end_v.vector2)
    
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
        offset_vector = vector2_subtract(self.vector2, center.vector2)
        scaled_offset = vector2_scale(offset_vector, scale_factor) 
        scaled_vector = vector2_add(center.vector2, scaled_offset)
        return self.to_Vec2(scaled_vector)

    def perp_norm(self):
        """
        Returns normalize perpendicular vector.
        """
        return self.to_Vec2(vector2_normalize(Vector2(-self.y, self.x)))