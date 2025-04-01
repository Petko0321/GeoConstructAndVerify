from sympy import symbols, groebner, simplify
from geocv import Point, Construction, Solution
from geocv import Vector, translate
import time

start_time = time.time()
# Example of translation of a vector
# initial distinct points
a1, b1, a2, b2, a3, b3 = symbols('a1, b1, a2, b2, a3, b3')
p1 = Point(a1, b1)
p2 = Point(a2, b2)
p3 = Point(a3, b3)
# construction
cons = Construction(p1, p2, p3)
# cons.not_collinear(p1, p2, p3)
# cons.solution.set_input_values(a1=0, b1=0, a2=1, b2=1, a3=2, b3=0)
line1 = cons.create_line(p1, p2)
v1 = Vector(p1, p2)
v2 = translate(v1, p3, optimized=True)
print("translated vector")
# # when all points are on the same line
# p4 = cons.point_on_object(line1)
# v4 = translate(v1, p4, cons, True)
# print("translated vector")
# visualize the points, the system, and variables
print("All points:")
for point in cons.points:
    print(point.to_str())
print("Construction system:")
print(cons.system)
print(cons.all_vars)
# create a solution
# print("Processing...")
# EXCECUTES SLOWLY
# solution = Solution(input_vars, [p.x, p.y], cons)
# print("End processing. Solution:")
# print(solution.reduced_groebner_basis)
# print("End")
# x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7, x8, y8, x9, y9, d10, d9, d8, d7, d6, d5, d4, d3, d2, d1 = symbols('x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7, x8, y8, x9, y9, d10, d9, d8, d7, d6, d5, d4, d3, d2, d1')
gens = cons.get_generators()
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")
start_time = time.time()
system = cons.solution.get_system()
print(system)
print("Proccesing")
gb = groebner(system, gens, domain='EX', order='grevlex' )
print(gb)
for i in gb:
    print(simplify(i))
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")
# End example