from sympy import symbols, groebner, solve
from geocv import Point, Construction
from geocv import perpendicular_line, midpoint, compass
import time
# Seperate a segment into golden ratio
# initial points - endpoints of the segment
a1, b1, a2, b2 = symbols('a1 b1 a2 b2')
p1 = Point(a1, b1)
p2 = Point(a2, b2)
# construction
cons = Construction(p1, p2)
line1 = cons.create_line(p1, p2)
line2 = perpendicular_line(p2, line1, True)
cr1 = cons.create_circle(p2, p1)
p3, _ = cons.intersect(line1, cr1)
cr2 = cons.create_circle(p3, p2)
p4, _ = cons.intersect(line1, cr2)
cr3 = cons.create_circle(p4, p1)
p5, p6 =  cons.intersect(cr3, line2)
p7, _ = cons.intersect(cr1, line2, True, p6)
m1 = midpoint(p5, p7)
cr4 = compass(p5, m1, p1)
_, p8 = cons.intersect(cr4, line1, True, p2)
# the point (p8) that is closer to p2 lies on the given segment
print(f"{p8.to_str()} seperates the given segment into golden ratio")
print("construction completed")
cons.set_as_output(p8)
# visualize the points, the system, and variables
print("All points:")
for point in cons.points:
    print(point.to_str())
print("Construction system:")
print(cons.solution.get_system())
# cons.solution.set_input_values(a1=0, b1=0, a2=1, b2=0)
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
print(f"Compute Groebner elapsed time: {elapsed_time:.2f} seconds")
start_time = time.time()
list_of_values = solve(gb, gens, dict=True)
for i in range(len(list_of_values)):
    cons.solution.values = list_of_values[i]
    print(cons.solution.values)
    print(f"Output object: {p8.to_str()}")
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Solve Groebner elapsed time: {elapsed_time:.2f} seconds")
# start_time = time.time()
# sol = solve(system, gens)
# print(sol)
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"Only solve elapsed time: {elapsed_time:.2f} seconds")

