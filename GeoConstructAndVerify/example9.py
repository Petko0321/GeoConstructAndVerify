from basics import Point, Construction, Solution
from utils import parallel_line, perpendicular_line, translate, Vector
from sympy import symbols, groebner, solve
import time
a1, b1, a2, b2, a3, b3 = symbols('a1 b1 a2 b2 a3 b3')
p1 = Point(a1, b1)
p2 = Point(a2, b2)
p3 = Point(a3, b3)
cons = Construction(p1, p2, p3)
line1 = cons.create_line(p1, p2)
line2 =  cons.create_line(p1, p3)
line3 = perpendicular_line(p3, line1, False)
p4 = cons.intersect(line1, line3)
_, p5, _ = translate(Vector(p3, p4), p4, False)
line4 = cons.create_line(p1, p5)
line5 = parallel_line(p2, line2)
center = cons.intersect(line4, line5)
circle1 = cons.create_circle(center, p2)
p4, p5 = cons.intersect(line1, circle1)
print("construction completed")
# visualize the points, the system, and variables
print("All points:")
for point in cons.points:
    print(point.to_str())
print("Construction system:")
print(cons.solution.get_system())
# cons.solution.set_input_values(a1=0, b1=0, a2=0, b2=4, a3=1, b3=2)
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
# End example
