from sympy import symbols
from basics import Point, Construction, Solution
from utils import perpendicular_line, midpoint, compass
# Seperate a segment into golden ratio
# initial points - endpoints of the segment
a1, b1, a2, b2 = symbols('a1 b1 a2 b2')
p1 = Point(a1, b1)
p2 = Point(a2, b2)
# construction
cons = Construction(p1, p2)
line1 = cons.create_line(p1, p2)
line2 = perpendicular_line(p2, line1, True, cons, True)
cr1 = cons.create_circle(p2, p1)
p3, _ = cons.intersect(line1, cr1, True)
cr2 = cons.create_circle(p3, p2)
p4, _ = cons.intersect(line1, cr2, True)
cr3 = cons.create_circle(p4, p1)
p5, p6 =  cons.intersect(cr3, line2, True)
p7, _ = cons.intersect(cr1, line2, True, p6)
m1 = midpoint(p5, p7, cons)
cr4 = compass(p5, m1, p1, cons, True)
_, p8 = cons.intersect(cr4, line1, True, p2)
# the point (p8) that is closer to p2 lies on the given segment
print(f"{p8.to_str()} seperates the given segment into golden ratio")
print("construction completed")
# visualize the points, the system, and variables
print("All points:")
for point in cons.points:
    print(point.to_str())
print("Construction system:")
print(cons.get_system())
print(cons.all_vars)

