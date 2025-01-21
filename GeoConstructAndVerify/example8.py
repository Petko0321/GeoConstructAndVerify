from basics import Point, Construction, Polygon
from utils import parallel_line, compass, circle_diameter, perpendicular_line
from sympy import symbols
# Construct a line parallel to the bases of a trapezoid that divides it into two similar trapezoids.
# initial points
a1, b1, b2, a3, b3, b4 = symbols('a1 b1 b2 a3 b3 b4')
p1 = Point(a1, b1)
p2 = Point(a1, b2)
p3 = Point(a3, b3)
p4 = Point(a3, b4)
trapezoid = Polygon(p1,p2,p3,p4)
#construction
cons = Construction(trapezoid)
l1 = cons.create_line(p1,p2)
l2 = cons.create_line(p1, p3)
l3 = cons.create_line(p1, p4)
cr1 = cons.create_circle(p3,p4)
_, p5 = cons.intersect(cr1, l2, True, p1)
# closer to p1 => lies on the diagonal
l4 = cons.create_line(p5, p2)
l5 = parallel_line(p3, l4, cons, True)
p6 = cons.intersect(l1, l5, True)
cr2 = compass(p1, p5, p6, cons, True)
p7, _ = cons.intersect(l1, cr2, True)
cr3 = circle_diameter(p2, p7, cons)
l6 = perpendicular_line(p6, l1, True, cons, True)
p8, p9 = cons.intersect(cr3, l6, True)
cr4 = compass(p6, p8, p1, cons, True)
_, p10 = cons.intersect(cr4, l1, True, p2)
# closer point lies on the base
l7 = parallel_line(p10, l3, cons, True)
l8 = cons.create_line(p2, p3)
p11 = cons.intersect(l7, l8, True)
l = parallel_line(p11, l1, cons, True)
p12 = cons.intersect(l3, l, True)
print("construction completed")
# visualize the points, the system, and variables
print("All points:")
for point in cons.points:
    print(point.to_str())
print("Construction system:")
print(cons.get_system())
print(cons.all_vars)


