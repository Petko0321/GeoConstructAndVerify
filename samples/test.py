from sympy import symbols, solve, groebner, Eq, simplify
import time
import itertools
import json
# a1, b1, a2, b2, a3, b3, d1, d2, d3, x1, y1, d4, x2, y2 = symbols('a1, b1, a2, b2, a3, b3, d1, d2, d3, x1, y1, d4, x2, y2')
# # sys = [Eq(d1*((a1 - a2)**2 + (b1 - b2)**2), 1), Eq(d2*((a1 - a3)**2 + (b1 - b3)**2), 1), Eq(d3*((a2 - a3)**2 + (b2 - b3)**2), 1), Eq((-a1 + x1)**2 + (-b1 + y1)**2, (-a1 + a3)**2 + (-b1 + b3)**2), Eq((-a2 + x1)**2 + (-b2 + y1)**2, (-a2 + a3)**2 + (-b2 + b3)**2), Eq(d4*((-a3 + x1)**2 + (-b3 + y1)**2), 1), Eq(a1*b2 - a2*b1 + x2*(b1 - b2) + y2*(-a1 + a2), 0), Eq(-a3*y1 + b3*x1 + x2*(-b3 + y1) + y2*(a3 - x1), 0)]
# # values = {a1: 1, b1: 1, a2: 3, b2: 2, a3: 4, b3: 5}
# # system = [(eq.lhs - eq.rhs).subs(values) for eq in sys]
# # print(system)
# # start_time = time.time()
# # solution = solve(system, x1, y1, x2, y2, d1, d2, d3, d4)
# # print(solution)
# # end_time = time.time()
# # elapsed_time = end_time - start_time
# # print(f"Elapsed time: {elapsed_time} seconds")

# # start_time = time.time()
# # gb = groebner(system, x1, y1, x2, y2, d4, d1, d2, d3, domain='EX', order='lex')
# # print(gb)
# # end_time = time.time()
# # elapsed_time = end_time - start_time
# # print(f"Elapsed time: {elapsed_time} seconds")

# # start_time = time.time()
# # system = [x1 - solution[0][0], y1 - solution[0][1], x2 - solution[0][2], y2 - solution[0][3]]
# # # print(system)
# # # solution = solve(system, x1, y1, x2, y2, d1, d2, d3, d4)
# # gb = groebner(system, x1, y1, x2, y2, d4, d1, d2, d3, domain='EX', order='lex')
# # print(gb)
# # end_time = time.time()
# # elapsed_time = end_time - start_time
# # print(f"Elapsed time: {elapsed_time} seconds")
# from sympy import symbols, solve, groebner, Eq, simplify
# import time
# x1, y1, x2, y2 = symbols('x1 y1 x2 y2')
# m1, n1, m2, n2, r1, r2, d = symbols('m1, n1, m2, n2, r1, r2, d')
# eq1 = (x1 - m1)**2 + (y1 - n1)**2 - r1**2
# eq2 = (x1 - m2)**2 + (y1 - n2)**2 - r2**2
# eq3 = (x2 - m1)**2 + (y2 - n1)**2 - r1**2
# eq4 = (x2 - m2)**2 + (y2 - n2)**2 - r2**2
# system = [eq1 - eq2, eq1 + eq2, eq3 - eq4, eq3 + eq4, d*((x1-x2)**2+(y1-y2)**2) - 1]
# # print(solve(system, x1, y1, x2, y2, d))
# start_time = time.time()
# gb = groebner(system, x1, y1, x2, y2, d, domain='EX')
# print(gb)
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"Elapsed time: {elapsed_time} seconds")
# for eq in gb:
#     print(simplify(eq))
x1, y1, x2, y2, x3, y3, d4, d5, d6 = symbols('x1 y1 x2 y2 x3 y3 d4 d5 d6')
list_of_gens = [[x1, y1], [x2, y2], [x3, y3], [d6], [d5], [d4]]
list_of_priorities = []
elapsed_times = []
i = 0
for i in range(120):
    with open(f"constructions\\geogebra\\construction1_computations_lex{i}.json", "r") as f1:
        gb_data = json.load(f1)
    list_of_priorities.append([symbols(var) for var in gb_data["variables"]])
    elapsed_times.append(gb_data["elapsed_time"])
print(list_of_priorities)
print(elapsed_times)
for i in range(len(list_of_priorities)):
    list_of_priorities[i] = [str(var) for var in list_of_priorities[i]]
lex_order_data = {
    "list of priorities": [list_of_priorities],
    "elapsed times": elapsed_times
}
print(lex_order_data["list of priorities"])
with open(f"constructions\\geogebra\\constr1_permutations_lex_order_data.json", "w") as f:
        json.dump(lex_order_data, f, indent=4)
# for perm in itertools.permutations(list_of_gens):
#     current_gens = []
    

