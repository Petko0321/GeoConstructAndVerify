from geocv import Point, Construction
from geocv import perpendicular_bisector
from sympy import symbols, groebner, solve, Symbol
import json
import time
# Construction of angle bisector
# given points:
a1, b1, a2, b2, a3, b3 = symbols('a1, b1, a2, b2, a3, b3', real=True)
p1 = Point(a1, b1)
p2 = Point(a2, b2)
p3 = Point(a3, b3)

# construction 1
start_time = time.time()
cons1 = Construction(p1, p2, p3)
cons1.not_collinear(p1, p2, p3)
line1 = cons1.create_line(p1, p2)
line12 = cons1.create_line(p2, p3)
circle1 = cons1.create_circle(p1, p3)
_, p4 = cons1.intersect(line1, circle1, True, p2)
ang_bis1 = perpendicular_bisector(p3, p4)
p6 = cons1.intersect(ang_bis1, line12, True)
cons1.set_as_output(p6)
print("construction 1 completed")
# visualize the points, the system, and variables
print("All points:")
for point in cons1.points:
    print(point.to_str())
print("Construction system:")
system1 = cons1.solution.get_system()
print(system1)
print(cons1.all_vars)
print("Solution 1:")
print(cons1.solution.system)
print(cons1.solution.input_vars)
print(cons1.solution.output_vars)
print(cons1.solution.auxiliary_vars)
print(cons1.solution.synthetic_vars)
generators = cons1.get_generators()
print(system1)
system1 = [str(eq) for eq in system1]
print(system1)
with open("constructions\\geogebra\\constr1_system.json","w") as f:
    json.dump(system1, f, indent=4)
print("Системата е записана успешно!")

# A1A2 =(a1-a2)**2+(b1-b2)**2
# A1A3 = (a1-a3)**2+(b1-b3)**2
# cons1.add_equation(cons1.output_object[0].coordinates[0]*(A1A2 + A1A3)-a2*A1A3 - a3*(A1A2))
# cons1.add_equation(cons1.output_object[0].coordinates[1]*(A1A2 + A1A3)-b2*A1A3 - b3*(A1A2))
# cons1.solution.set_input_values(a1=1, b1=1, a2=4, b2=0, a3=2, b3=4)
# system1 = cons1.solution.get_system()
# print(system1)
# start_time = time.time()
# generators = cons1.get_generators()
# sol = solve(system1, generators)
# # print(sol)
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"Elapsed time: {elapsed_time:.2f} seconds")
# start_time = time.time()
# x1, y1, x2, y2, y3, x3, d6, d5, d4, d3, d2, d1 = generators
# gb1 = groebner(system1, *generators, domain="EX", order="lex")
# print(gb1)
# gb_data1 = {
#     "basis": [str(poly) for poly in gb1],  # Запазване на полиномите като низове
#     "variables": [str(var) for var in gb1.gens],  # Променливите
#     "order": str(gb1.order),  # Реда (lex, grlex, grevlex)
#     "domain": str(gb1.domain)  # Полиномиалното поле (EX, ZZ, QQ и т.н.)
# }
# with open("construction_gb_1_1.json", "w") as f:
#     json.dump(gb_data1, f, indent=4)
# print("Грьобнеровата база е записана успешно!")
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"Elapsed time: {elapsed_time:.2f} seconds")

# # construction 2
# cons2 = Construction(p1, p2, p3)
# start_time = time.time()
# cons2.not_collinear(p1, p2, p3)
# line2 = cons2.create_line(p1, p3)
# line22 = cons2.create_line(p2, p3)
# circle2 = cons2.create_circle(p1, p2)
# _, p4 = cons2.intersect(line2, circle2, True, p3)
# ang_bis2 = perpendicular_bisector(p2, p4)
# p6 = cons2.intersect(ang_bis2, line22, True)
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"Elapsed time: {elapsed_time:.2f} seconds")
# print("construction 2 completed")
# # visualize the points, the system, and variables
# print("All points:")
# for point in cons2.points:
#     print(point.to_str())
# print("Construction system:")
# system2 = cons2.solution.get_system()
# print(system2)
# print(cons2.all_vars)
# sol2 = cons2.solution
# print("Solution 2:")
# print(sol2.input_vars)
# print(sol2.output_vars)
# print(sol2.auxiliary_vars)
# print(sol2.synthetic_vars)
# # sol2.set_input_values(a1=1, b1=1, a2=4, b2=0, a3=2, b3=4)
# system2 = sol2.get_system()
# print(system2)
# generators = cons2.get_generators()
# # x3 = generators[4]
# # y3 = generators[5]
# # print(x3)
# # print(y3)
# start_time = time.time()
# # sol = solve(system2, generators, dict=True)
# # for i in sol:
# #     print(x3 + i[x3])
# #     print(y3 + i[y3])
# gb2 = groebner(system2, generators, domain="EX", order="grevlex")
# print(gb2)
# gb_data2 = {
#     "basis": [str(poly) for poly in gb2],  # Запазване на полиномите като низове
#     "variables": [str(var) for var in gb2.gens],  # Променливите
#     "order": str(gb2.order),  # Реда (lex, grlex, grevlex)
#     "domain": str(gb2.domain)  # Полиномиалното поле (EX, ZZ, QQ и т.н.)
# }
# with open("construction_gb_2_1.json", "w") as f:
#     json.dump(gb_data2, f, indent=4)
# print("Грьобнеровата база е записана успешно!")
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"Elapsed time: {elapsed_time:.2f} seconds")

# construction 3
# cons3 = Construction(p1, p2, p3)
# cons3.not_collinear(p1, p2, p3)
# line31 = cons3.create_line(p1, p2)
# line32 = cons3.create_line(p1, p3)
# line33 = cons3.create_line(p2, p3)
# arib1 = cons3.get_arbitrary_point(line31)
# cons3.not_coinciding(p1, arib1)
# circle3 = cons3.create_circle(p1, arib1)
# _, p4 = cons3.intersect(line32, circle3, True, p3)
# ang_bis3 = perpendicular_bisector(arib1, p4)
# p6 = cons3.intersect(ang_bis3, line33, True)
# print("construction 3 completed")
# # visualize the points, the system, and variables
# print("All points:")
# for point in cons3.points:
#     print(point.to_str())
# print("Construction system:")
# print(cons3.all_vars)
# x4, y4 = symbols('x4 y4')
# sol3 = cons3.solution
# print("Solution 3:")
# print(sol3.system)
# print(sol3.input_vars)
# print(sol3.output_vars)
# print(sol3.auxiliary_vars)
# print(sol3.synthetic_vars)
# # A1A2 =(a1-a2)**2+(b1-b2)**2
# # A1A3 = (a1-a3)**2+(b1-b3)**2
# # sol3.system.append(x6*(A1A2 + A1A3)-a2*A1A3 - a3*(A1A2))
# # sol3.system.append(y6*(A1A2 + A1A3)-b2*A1A3 - b3*(A1A2))
# # sol3.set_input_values(a1=1, b1=1, a2=4, b2=0, a3=2, b3=4)
# system3 = sol3.get_system()
# print(system3)
# start_time = time.time()
# generators = cons3.get_generators()
# print(generators)
# x1, y1, x2, y2, x3, y3, x4, y4, d7, d6, d5, d4, d3, d2, d1 = generators
# generators = [x1, y1, x2, y2, x3, y3, x4, y4, d7, d6, d5, d4]
# i = 0
# for perm in itertools.permutations(generators):
#     start_time = time.time()
#     gb3 = groebner(system3, *perm, domain="EX", order="lex")
#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     gb_data3 = {
#         # Запазване на полиномите като низове
#         "basis": [str(poly) for poly in gb3],
#         "variables": [str(var) for var in gb3.gens],  # Променливите
#         "order": str(gb3.order),  # Реда (lex, grlex, grevlex)
#         "domain": str(gb3.domain),  # Полиномиалното поле (EX, ZZ, QQ и т.н.)
#         "elapsed_time": float(elapsed_time)  # Време на изпълнение
#     }
#     with open(f"constructions\\geogebra\\construction3_computations_lex{i}.json", "w") as f:
#         json.dump(gb_data3, f, indent=4)
#     print("Грьобнеровата база е записана успешно!")
#     i += 1


# # sol = solve(system3, generators)
# # print(sol)
# # for i in sol:
# #     print(i[x4])
# #     print(i[y4])
# gb3 = groebner(system3, x1, y1, x2, y2, x3, y3, d5, d6, d7, x4, y4, d4, d3, d2, d1, domain="EX", order="grevlex")
# print(gb3)
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"Elapsed time: {elapsed_time:.2f} seconds")
# gb_data3 = {
#     "basis": [str(poly) for poly in gb3],  # Запазване на полиномите като низове
#     "variables": [str(var) for var in gb3.gens],  # Променливите
#     "order": str(gb3.order),  # Реда (lex, grlex, grevlex)
#     "domain": str(gb3.domain),  # Полиномиалното поле (EX, ZZ, QQ и т.н.)
#     "elapsed_time": float(elapsed_time)  # Време на изпълнение
# }
# with open("constructions\\geogebra\\construction3_grevlex1.json", "w") as f:
#     json.dump(gb_data3, f, indent=4)
# print("Грьобнеровата база е записана успешно!")
# start_time = time.time()
# gb3 = groebner(system3, x1, y1, x2, y2, x3, y3, d5, d6, d7, x4, y4, d4, d3, d2, d1, domain="EX", order="grevlex")
# print(gb3)
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"Elapsed time: {elapsed_time:.2f} seconds")
# gb_data3 = {
#     "basis": [str(poly) for poly in gb3],  # Запазване на полиномите като низове
#     "variables": [str(var) for var in gb3.gens],  # Променливите
#     "order": str(gb3.order),  # Реда (lex, grlex, grevlex)
#     "domain": str(gb3.domain),  # Полиномиалното поле (EX, ZZ, QQ и т.н.)
#     "elapsed_time": float(elapsed_time)  # Време на изпълнение
# }
# with open("constructions\\geogebra\\construction3_lex111.json", "w") as f:
#     json.dump(gb_data3, f, indent=4)
# print("Грьобнеровата база е записана успешно!")
# End example
