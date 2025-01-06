from basics import Point, Construction, Triangle
from utils import perpendicular_line, compass, midpoint, parallel_line, construct_square
from sympy import symbols
# Construct a square with the same surface as given triangle
# initial points - vertices of the triangle
a1, b1, a2, b2, a3, b3 = symbols('a1 b1 a2 b2 a3 b3')
p1 = Point(a1, b1)
p2 = Point(a2, b2)
p3 = Point(a3, b3)
tr = Triangle(p1, p2, p3)
# construction
cons = Construction(tr)
line1 = cons.create_line(p1, p2)
h_p3 = perpendicular_line(p3, line1, False, cons, True)
h3 = cons.intersect(h_p3, line1, True)
m1 = midpoint(p3, h3, cons)
arib1 = cons.get_arbitrary_point(line1, 1)
line2 = cons.create_line(p1, arib1)
cr2 = compass(p3, m1, arib1, cons, True)
# d(p3,m1) = h_c/2
p4, _ = cons.intersect(cr2, line2, True, p1)
# p4 further intersecting point relative to p1
line3 = cons.create_line(arib1, p2)
line4 = parallel_line(p4, line3, cons, True)
p5 = cons.intersect(line1, line4, True)
cr3 = compass(p1, arib1, p5, cons, True)
p6, _ = cons.intersect(cr3, line1, True, p2)
# p6 further intersecting point relative to p2
p7 = midpoint(p2, p6, cons)
cr4 = cons.create_circle(p7, p2)
line5 = perpendicular_line(p7, line1, True, cons, True)
p8, _ = cons.intersect(cr4, line5, True)
square = construct_square(p7, p8, cons)
print("sqaure constructed")
# visualize the points, the system, and variables
print("All points:")
for point in cons.points:
    print(point.to_str())
print("Construction system:")
print(cons.get_system())
print(cons.all_vars)



