from basics import Point, Construction, Solution
from utils import perpendicular_bisector
from sympy import symbols, groebner
import time
# Construction of angle bisector
# given points:
a1, b1, a2, b2, a3, b3 = symbols('a1, b1, a2, b2, a3, b3')
p1 = Point(a1, b1)
p2 = Point(a2, b2)
p3 = Point(a3, b3)
# construction 1
# start_time = time.time()
# cons1 = Construction(p1, p2, p3)
# #cons1.not_on_same_line(p1, p2, p3)
# line1 = cons1.create_line(p1, p2)
# line12 = cons1.create_line(p2, p3)
# circle1 = cons1.create_circle(p1, p3)
# _, p4 = cons1.intersect(line1, circle1, True, p2)
# ang_bis1 = perpendicular_bisector(p3, p4)
# p5 = cons1.get_arbitrary_point(ang_bis1)
# p6 = cons1.intersect(ang_bis1, line12, True)
# x6, y6 = symbols('x6, y6')
# sol1 = Solution(cons1, [x6, y6])
# print("construction 1 completed")
# # visualize the points, the system, and variables
# print("All points:")
# for point in cons1.points:
#     print(point.to_str())
# print("Construction system:")
# system1 = cons1.get_system()
# print(system1)
# print(cons1.all_vars)
# print("Solution 1:")
# print(sol1.system)
# print(sol1.input_vars)
# print(sol1.output_vars)
# print(sol1.auxiliary_vars)
# print(sol1.synthetic_vars)
# sol1.set_input_values(a1=1, b1=1, a2=4, b2=0, a3=2, b3=4)
# system1 = sol1.system
# print(system1)
# start_time = time.time()
# generators = sol1.synthetic_vars + sol1.auxiliary_vars + sol1.output_vars
# gb1 = groebner(system1, generators, domain="EX", order="grevlex")
# print(gb1)
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"Elapsed time: {elapsed_time:.2f} seconds")
# # construction 2
# cons2 = Construction(p1, p2, p3)
# #cons2.not_on_same_line(p1, p2, p3)
# line2 = cons2.create_line(p1, p3)
# line22 = cons2.create_line(p2, p3)
# circle2 = cons2.create_circle(p1, p2)
# _, p4 = cons2.intersect(line2, circle2, True, p3)
# ang_bis2 = perpendicular_bisector(p2, p4)
# p5 = cons2.get_arbitrary_point(ang_bis2)
# p6 = cons2.intersect(ang_bis2, line22, True)
# elapsed_time = end_time - start_time
# print(f"Elapsed time: {elapsed_time:.2f} seconds")
# print("construction 2 completed")
# # visualize the points, the system, and variables
# print("All points:")
# for point in cons2.points:
#     print(point.to_str())
# print("Construction system:")
# system2 = cons2.get_system()
# print(system2)
# print(cons2.all_vars)
# sol2 = Solution(cons2, [x6, y6], optimized=True)
# print("Solution 2:")
# print(sol2.system)
# print(sol2.input_vars)
# print(sol2.output_vars)
# print(sol2.auxiliary_vars)
# print(sol2.synthetic_vars)
# sol2.set_input_values(a1=1, b1=1, a2=4, b2=0, a3=2, b3=4)
# system2 = sol2.system
# print(system2)
# start_time = time.time()
# generators = sol2.synthetic_vars + sol2.auxiliary_vars + sol2.output_vars
# print(generators)
# gb2 = groebner(system2, generators, domain="EX", order="grevlex")
# print(gb2)
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"Elapsed time: {elapsed_time:.2f} seconds")
# end_time = time.time()
# #print(gb1==gb2)

# construction 3
cons3 = Construction(p1, p2, p3)
#cons2.not_on_same_line(p1, p2, p3)
line31 = cons3.create_line(p1, p2)
line32 = cons3.create_line(p1, p3)
line33 = cons3.create_line(p2, p3)
circle3 = cons3.create_circle(p1, cons3.get_arbitrary_point(line31))
_, p4 = cons3.intersect(line32, circle3, True, p3)
ang_bis3 = perpendicular_bisector(p2, p4)
# p5 = cons2.get_arbitrary_point(ang_bis2)
p6 = cons3.intersect(ang_bis3, line33, True)
print("construction 3 completed")
# visualize the points, the system, and variables
print("All points:")
for point in cons3.points:
    print(point.to_str())
print("Construction system:")
system3 = cons3.get_system()
print(system3)
print(cons3.all_vars)
x6, y6 = symbols('x6 y6')
sol3 = Solution(cons3, [x6, y6], optimized=True)
print("Solution 2:")
print(sol3.system)
print(sol3.input_vars)
print(sol3.output_vars)
print(sol3.auxiliary_vars)
print(sol3.synthetic_vars)
sol3.set_input_values(a1=1, b1=1, a2=4, b2=0, a3=2, b3=4)
system3 = sol3.system
print(system3)
start_time = time.time()
generators = sol3.synthetic_vars + sol3.auxiliary_vars + sol3.output_vars
print(generators)
gb3 = groebner(system3, generators, domain="EX", order="grevlex")
print(gb3)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")
end_time = time.time()
# print("Processing...:)")
# start_time = time.time()
# gb = groebner(system1, domain="RR", order="grevlex")
# print(gb)
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"Elapsed time: {elapsed_time:.2f} seconds")
# ideal1 =  [eq.lhs - eq.rhs for eq in system1]
# print(ideal1)
# ideal2 = [eq.lhs - eq.rhs for eq in system2]
# print(ideal2)
