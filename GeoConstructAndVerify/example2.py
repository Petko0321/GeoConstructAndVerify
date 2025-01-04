from basics import Point, Construction
from utils import parallel_line
from sympy import symbols
# Example of separating a segment into n equal parts
# initial points - the vertices of the segment
a1, b1, a2, b2 = symbols('a1 b1 a2 b2')
p1 = Point(a1, b1, construction=None)
p2 = Point(a2, b2, construction=None)
print("Enter n:")
n = int(input())
# construction
cons = Construction([p1, p2])
line1 = cons.create_line(p1, p2)
arib1 = cons.get_arbitrary_point(line1, False)
line2 = cons.create_line(p1, arib1)
current_center = arib1
current_point_on_circle = p1
points_on_line2 = []
for i in range(1, n):
    print(f"Step {i}")
    points_on_line2.append(current_center)
    cr = cons.create_circle(current_center, current_point_on_circle)
    p3, _ = cons.intersect(cr, line2, True)
    current_point_on_circle = current_center
    current_center = p3
print("End for loop")
line3 = cons.create_line(current_center, p2)
points = []
for point in points_on_line2:
    print(f"Step {point.to_str()}")
    current_line = parallel_line(point, line3, cons, True)
    p = cons.intersect(current_line, line1, True)
    points.append(p)
print(f"The points which seperate the segment into {n} equal parts are:")
for point in points:
    print(point.to_str())
print("finished")
# visualize the points, the system, and variables
print("All points:")
for point in cons.points:
    print(point.to_str())
print("Construction system:")
print(cons.get_system())
print(cons.all_vars)
# End example