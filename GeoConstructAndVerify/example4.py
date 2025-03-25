from basics import Point, Construction, Triangle
from utils import perpendicular_line, compass, midpoint, parallel_line, construct_square
from sympy import symbols, groebner, solve
import time
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
h_p3 = perpendicular_line(p3, line1, False)
h3 = cons.intersect(h_p3, line1)
m1 = midpoint(p3, h3)
arib1 = cons.get_arbitrary_point(line1, 1)
line2 = cons.create_line(p1, arib1)
cr2 = compass(p3, m1, arib1)
# d(p3,m1) = h_c/2
p4, _ = cons.intersect(cr2, line2, True, p1)
# p4 further intersecting point relative to p1
line3 = cons.create_line(arib1, p2)
line4 = parallel_line(p4, line3)
p5 = cons.intersect(line1, line4)
cr3 = compass(p1, arib1, p5)
p6, _ = cons.intersect(cr3, line1, True, p2)
# p6 further intersecting point relative to p2
p7 = midpoint(p2, p6)
cr4 = cons.create_circle(p7, p2)
line5 = perpendicular_line(p7, line1, True)
p8, _ = cons.intersect(cr4, line5)
square = construct_square(p7, p8)
print("sqaure constructed")
# visualize the points, the system, and variables
print("All points:")
for point in cons.points:
    print(point.to_str())
print("Construction system:")
print(cons.solution.get_system())
cons.solution.set_input_values(a1=0, b1=0, a2=4, b2=0, a3=1, b3=2)
gens = cons.get_generators()
start_time = time.time()
system = cons.solution.get_system()
print(system)
print(gens)
print("Proccesing")
gb = groebner(system, gens, domain='EX', order='grevlex')
print(gb)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")



