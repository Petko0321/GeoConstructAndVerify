from basics import Point, Construction, Circle, Line
from utils import circle_through_3_points, perpendicular_line
from sympy import symbols
# Example of construction the radical axis of two circles
# initial points
a1, b1, a2, b2, a3, b3, a4, b4 = symbols('a1 b1 a2 b2 a3 b3 a4 b4')
center1 = Point(a1, b1, construction=None)
p1 = Point(a2, b2, construction=None)
center2 = Point(a3, b3, construction=None)
p2 = Point(a4, b4, construction=None)
circle1 = Circle(center1, p1, construction=None)
circle2 = Circle(center2, p2, construction=None)
# construction
cons = Construction([circle1, circle2])
line1 = cons.create_line(center1, center2)
# p5 = cons.point_on_object(circle1)
# p6 = cons.point_on_object(circle2)
# p7 = cons.get_arbitrary_point(Line(p5, p6), 1)
# circle3 = circle_through_3_points(p5, p6, p7, cons, True)
# p8, p9 = cons.intersect(circle1, circle3, True)
# p10, p11 = cons.intersect(circle2, circle3, True)
# line2 = cons.create_line(p8, p9)
# line3 = cons.create_line(p10, p11)
# p12 = cons.intersect(line2, line3, True)
# radical_axis = perpendicular_line(p12, line1, False, cons, True)
p3 = 

