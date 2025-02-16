from sympy import symbols
from basics import Point, Construction, Solution
from utils import Vector, translate
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
cons.not_on_same_line(p1, p2, p3)
line1 = cons.create_line(p1, p2)
v1 = Vector(p1, p2)
_, p, v3 = translate(v1, p3, cons)
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
print(cons.get_system())
print(cons.all_vars)
# create a solution
# print("Processing...")
# EXCECUTES SLOWLY
# solution = Solution(input_vars, [p.x, p.y], cons)
# print("End processing. Solution:")
# print(solution.reduced_groebner_basis)
# print("End")
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")
# End example