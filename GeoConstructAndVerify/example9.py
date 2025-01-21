from basics import Point, Construction, Solution
from utils import perpendicular_bisector
from sympy import symbols
a1, b1, a2, b2 = symbols('a1 b1 a2 b2')
p1 = Point(a1, b1)
p2 = Point(a2, b2)
cons = Construction(p1, p2)
line1 = cons.create_line(p1, p2)
perp_bis = perpendicular_bisector(p1, p2, cons, True)
p3 = cons.get_arbitrary_point(perp_bis)
circle1 = cons.create_circle(p3, p2)
p4, p5 = cons.intersect(line1, circle1, True)
print(p4.to_str())
print(p5.to_str())
print("construction completed")
# visualize the points, the system, and variables
print("All points:")
for point in cons.points:
    print(point.to_str())
print("Construction system:")
print(cons.get_system())
print(cons.all_vars)
solution = Solution(cons, [a1, b1, a2, b2], [p4.x, p4.y])
print(solution.reduced_groebner_basis) 
