from basics import Point, Construction, Polygon
from utils import parallel_line, compass, circle_by_diameter, perpendicular_line
from sympy import symbols, groebner
import time
# Construct a line parallel to the bases of a trapezoid that divides it into two similar trapezoids.
# initial points
a1, b1, a2, b2, a3, b3, a4, b4 = symbols('a1, b1, a2, b2, a3, b3, a4, b4')
p1 = Point(a1, b1)
p2 = Point(a2, b2)
p3 = Point(a3, b3)
p4 = Point(a4, b4)
trapezoid = Polygon(p1,p2,p3,p4)
#construction
start_time = time.time()
cons = Construction(trapezoid)
cons.solution.set_input_values(a1=0, b1=0, a2=4, b2=0, a3=2, b3=3, a4=3, b4=3)
l1 = cons.create_line(p1, p2)
l2 = cons.create_line(p1, p3)
l3 = cons.create_line(p1, p4)
cr1 = cons.create_circle(p3,p4)
_, p5 = cons.intersect(cr1, l2, point_coordinator=p1)
# closer to p1 => lies on the diagonal
l4 = cons.create_line(p5, p2)
l5 = parallel_line(p3, l4)
p6 = cons.intersect(l1, l5)
cr2 = compass(p1, p5, p6)
p7, _ = cons.intersect(l1, cr2)
cr3 = circle_by_diameter(p2, p7)
l6 = perpendicular_line(p6, l1, True)
p8, p9 = cons.intersect(cr3, l6)
cr4 = compass(p6, p8, p1)
_, p10 = cons.intersect(cr4, l1, point_coordinator=p2)
# closer point lies on the base
l7 = parallel_line(p10, l3)
l8 = cons.create_line(p2, p3)
p11 = cons.intersect(l7, l8)
l = parallel_line(p11, l1)
p12 = cons.intersect(l3, l)
cons.set_as_ouput(l)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")
print("construction completed")
# visualize the points, the system, and variables
print("All points:")
for point in cons.points:
    print(point.to_str())
print(f"Output object: {cons.output_object[0].equation}")
print("Construction system:")
print(cons.system)
print(cons.all_vars)
system = cons.solution.get_system()
print(system)
start_time = time.time()
generators = cons.get_generators()
print(generators)
print("Proccesing")
gb = groebner(system, generators, domain='EX', order='grevlex' )
print(gb)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")
# End example

