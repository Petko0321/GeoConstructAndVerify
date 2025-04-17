from geocv import Point, Construction, Circle
from geocv import perpendicular_line, compass
from sympy import symbols, groebner
import time
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
line2 = perpendicular_line(center1, line1, True)
cr3 = compass(center2, p2, center1)
p3, _ = cons.intersect(line2, cr3)
# p3 = cons.intersect(line2, cr3, return_any_of_two=True)
cr = cons.create_circle(p3, p1)
print(f"Circle({p3.x}, {p3.y}) ({p1.x}, {p1.y})")
print("circle constructed")
cons.set_as_output(cr)
# visualize the points, the system, and variables
print("All points:")
for point in cons.points:
    print(point.to_str())
print("Construction system:")
print(cons.solution.get_system())
# cons.solution.set_input_values(a1=0, b1=0, a2=2, b2=0, a3=5, b3=0, a4=5, b4=1)
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
print(f"Output object: {cons.output_object[0].equation}")

