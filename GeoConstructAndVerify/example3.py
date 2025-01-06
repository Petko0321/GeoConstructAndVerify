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
cons = Construction(circle1, circle2)
line1 = cons.create_line(center1, center2)
line2 = cons.create_line(p1, p2)
p3 = cons.get_arbitrary_point(line2, 1)
circle3 = circle_through_3_points(p1, p2, p3, cons, True)
p4, p5 = cons.intersect(circle1, circle3, True)
p6, p7 = cons.intersect(circle2, circle3, True)
line2 = cons.create_line(p4, p5)
line3 = cons.create_line(p6, p7)
p8 = cons.intersect(line2, line3, True)
radical_axis = perpendicular_line(p8, line1, False, cons, True)
print("The radical axis completed")
# visualize the points, the system, and variables
print("All points:")
for point in cons.points:
    print(point.to_str())
print("Construction system:")
print(cons.get_system())
print(cons.all_vars)