from basics import Point, Construction, Triangle
from utils import perpendicular_line, compass, midpoint, parallel_line
from sympy import symbols
# Construct a square with the same surface as given triangle
# initial points
a1, b1, a2, b2, a3, b3 = symbols('a1 b1 a2 b2 a3 b3')
p1 = Point(a1, b1, construction=None)
p2 = Point(a2, b2, construction=None)
p3 = Point(a3, b3, construction=None)
tr = Triangle(p1, p2, p3, construction=None)
# construction
cons = Construction([tr])
line1 = cons.create_line(p1, p2)
h_p3 = perpendicular_line(p3, line1, False, cons, True)
h3 = cons.intersect(h_p3, line1, True)
m1 = midpoint(p3, h3, cons)
arib1 = cons.get_arbitrary_point(line1, 1)
line2 = cons.create_line(p1, arib1)
cr1 = cons.create_circle(p1, arib1)
p4, p5 = cons.intersect(cr1, line2, True)
cr2 = compass(p3, m1, p4, cons, True)
p6, _ = cons.intersect(cr2, line2, p1, True)
line3 = cons.create_line(arib1, p2)
line4 = parallel_line(line3, p6)
p7 = cons.intersect(line1, line4)
cr3 = compass(p1, arib1, p7)
p8, _ = cons.intersect(cr3, line1, p2)
p9 = midpoint(p2, p8)
cr4 = cons.create_circle(p9, p8)
line5 = perpendicular_line(p7, line1, True, cons, True)
p10, p11 = cons.intersect(cr4, line5)
print(f"{p7.to_str} and {p10.to_str()} are two verticies of the square")



