__version__ = "0.1.0"

# Import main classes from basics
from .basics import (
    Construction, Point, Line, Circle, 
    Polygon, Triangle, Square, Solution,
    AribitaryPoint, Geometrical_obj, coincide_points
)

# Import utility functions
from .utils import (
    perpendicular_bisector, midpoint, angle_bisector, 
    perpendicular_line, parallel_line, translate_vector, 
    translate, compass, circle_through_3_points, 
    circle_by_diameter, construct_square, 
    simplify_expressions, reduce_quadratics, Vector
)

__all__ = [
    "Construction", "Point", "Line", "Circle", "Polygon", "Triangle", "Square", "Solution",
    "perpendicular_bisector", "midpoint", "angle_bisector", "perpendicular_line", "parallel_line",
    "translate_vector", "translate", "compass", "circle_through_3_points", "circle_by_diameter",
    "construct_square", "simplify_expressions", "reduce_quadratics", "Vector"
]
