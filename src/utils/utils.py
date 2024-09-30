from pyray import *

def vector2_center_scale(vector: Vector2, center: Vector2, scale_factor: float) -> Vector2:
    """
    Scale vector using center reference(vector) by scale factor.
    """
    offset_vector = vector2_subtract(vector, center) #traslation
    scaled_offset = vector2_scale(offset_vector, scale_factor) 
    scaled_vector = vector2_add(center, scaled_offset)
    return scaled_vector
