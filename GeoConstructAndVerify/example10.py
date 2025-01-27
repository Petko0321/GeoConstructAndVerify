from basics import Point, Construction
from utils import perpendicular_bisector
from sympy import symbols
# Construction of angle bisector
# given points:
a1, b1, a2, b2, a3, b3 = symbols('a1, b1, a2, b2, a3, b3')
p1 = Point(a1, b1)
p2 = Point(a2, b2)
p3 = Point(a3, b3)
# construction 1
cons1 = Construction(p1, p2, p3)
line1 = cons1.create_line(p1, p2)
line12 = cons1.create_line(p2, p3)
circle1 = cons1.create_circle(p1, p3)
p4, _ = cons1.intersect(line1, circle1, True)
ang_bis1 = perpendicular_bisector(p3, p4, cons1, True)
#p5 = cons1.get_arbitrary_point(ang_bis1)
p6 = cons1.intersect(ang_bis1, line12, True)
print("construction 1 completed")
# visualize the points, the system, and variables
print("All points:")
for point in cons1.points:
    print(point.to_str())
print("Construction system:")
system1 = cons1.get_system()
print(system1)
print(cons1.all_vars)
# construction 2
cons2 = Construction(p1, p2, p3)
line2 = cons2.create_line(p1, p3)
line22 = cons2.create_line(p2, p3)
circle2 = cons2.create_circle(p1, p2)
p4, _ = cons2.intersect(line2, circle2, True)
ang_bis2 = perpendicular_bisector(p2, p4, cons2, True)
p5 = cons2.get_arbitrary_point(ang_bis2)
p6 = cons1.intersect(ang_bis2, line22, True)
print("construction 2 completed")
# visualize the points, the system, and variables
print("All points:")
for point in cons2.points:
    print(point.to_str())
print("Construction system:")
system2 = cons2.get_system()
print(system2)
print(cons2.all_vars)