from basics import Point, Construction, Triangle
from utils import angle_bisector, perpendicular_line, compass, midpoint, parallel_line, construct_square
from sympy import symbols, groebner, solve
import time
# Construct three circles with centers the vertices of a given triangle each two of which touch eachother
# initial points - vertices of the triangle
a1, b1, a2, b2, a3, b3 = symbols('a1 b1 a2 b2 a3 b3')
p1 = Point(a1, b1)
p2 = Point(a2, b2)
p3 = Point(a3, b3)
tr = Triangle(p1, p2, p3)
# construction
cons = Construction(tr)
line1 = cons.create_line(p1, p2)
line2 = cons.create_line(p1, p3)
line3 = cons.create_line(p2, p3)
ang_bis1 = angle_bisector(p2, p1, p3)
ang_bis2 = angle_bisector(p1, p2, p3)
p4 = cons.intersect(ang_bis1, ang_bis1)
line4 = perpendicular_line(p4, line1, False)
p5 = cons.intersect(line1, line4)
cr1 = cons.create_circle(p1, p5)
# circle 1
cr2 = cons.create_circle(p2, p5)
# circle 2
_, p6 = cons.intersect(cr1, line2, True, p3)
# closer point (p6) relative to p3 lies on the side p1p3
cr3 = cons.create_circle(p3, p6)
# circle 3
print("construction completed")
cons.set_as_output(p6)
# visualize the points, the system, and variables
print("All points:")
for point in cons.points:
    print(point.to_str())
print("Construction system:")
print(cons.solution.get_system())
cons.solution.set_input_values(a1=0, b1=0, a2=5, b2=0, a3=2, b3=4)
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
sol = solve(gb, gens)
print(sol)
print(f"Output object: {p6.to_str()}")



