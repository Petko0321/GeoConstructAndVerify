from basics import Point, Construction, Circle
from utils import perpendicular_line, compass, midpoint, parallel_line, construct_square
from sympy import symbols
# Construct a circle with surface equal to the sum of the surfaces of two given circles
# initial points and circles
a1, b1, a2, b2, a3, b3, a4, b4 = symbols('a1 b1 a2 b2 a3 b3 a4 b4')
center1 = Point(a1,b1)
p1 = Point(a2,b2)
center2 = Point(a3,b3)
p2 = Point(a4,b4)
cr1 = Circle(center1, p1)
cr2 = Circle(center2, p2)
# construction
cons = Construction(cr1, cr2)
line1 = cons.create_line(center1, p1)
line2 = perpendicular_line(center1, line1, True, cons, True)
cr3 = compass(center2, p2, center1, cons, True)
p3, _ = cons.intersect(line2, cr3, True)
cr = cons.create_circle(p3, p1)
print(f"Circle({p3.x}, {p3.y}) ({p1.x}, {p1.y})")
print("circle constructed")
# visualize the points, the system, and variables
print("All points:")
for point in cons.points:
    print(point.to_str())
print("Construction system:")
print(cons.get_system())
print(cons.all_vars)

