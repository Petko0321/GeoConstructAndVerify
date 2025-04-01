from sympy import symbols, solve
from geocv import Point, Construction, Solution
from geocv import Vector, translate
import time

start_time = time.time()
# Example of translation of a vector
# initial distinct points
c1, d1, c2, d2 = symbols('c1 d1 c2 d2')
input_vars = [c1, d1, c2, d2]
p1 = Point(c1, d1, construction=None)
p2 = Point(c2, d2, construction=None)
# construction
cons = Construction(p1, p2)
line1 = cons.create_line(p1, p2)
crcl1 = cons.create_circle(p1, p2)
res3 = cons.intersect(line1, crcl1)
p3, p4 = 
print("All points:")
for point in cons.points:
    print(point.to_str())
print("Construction system:")
print(cons.get_system())
print(cons.all_vars)
# create a solution
print("Processing...")
# EXCECUTES SLOWLY
solution = Solution(input_vars, [p3.x, p3.y], cons)
print("End processing. Solution:")
print(solution.reduced_groebner_basis)
print("End")
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")
# End example