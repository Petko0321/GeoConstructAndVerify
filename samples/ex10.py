import json
from sympy import symbols, Symbol, sympify, groebner, fraction
from utils import reduce_quadratics, simplify_expressions
import time

start_time = time.time()
with open("construction_gb_1_1.json", "r") as f1:
    gb_data = json.load(f1)
variables = [symbols(var) for var in gb_data["variables"]]
polynomials = [sympify(poly) for poly in gb_data["basis"]]
order = gb_data["order"]
domain = gb_data["domain"]
gb1 = groebner(polynomials, *variables, order=order, domain=domain)
num_polynomials, denom_polynomials = simplify_expressions(gb1)
print(num_polynomials)
num_polynomials = reduce_quadratics(num_polynomials, variables)
print(num_polynomials)
# groebner_basis = [None]*len(num_polynomials)
# for i in range(len(num_polynomials)):
#     groebner_basis[i] = num_polynomials[i] / denom_polynomials[i]
# reduced_gb1 = groebner(groebner_basis, *variables, order=order, domain=domain)
# print(reduced_gb1)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Simplify elapsed time: {elapsed_time:.2f} seconds")

# compare1 = []
# for eq in gb1:
#     symb1 = eq.free_symbols
#     if (Symbol("x3") in symb1 or Symbol("y3") in symb1) and Symbol("x1") not in symb1 and Symbol("y1") not in symb1 and Symbol("x2") not in symb1 and Symbol("y2") not in symb1:
#         compare1.append(eq)
# print(compare1)

# with open("construction_gb_2.json", "r") as f2:
#     gb_data = json.load(f2)
# variables = [symbols(var) for var in gb_data["variables"]]
# polynomials = [sympify(poly) for poly in gb_data["basis"]]
# order = gb_data["order"]
# domain = gb_data["domain"]
# gb2 = groebner(polynomials, *variables, order=order, domain=domain)

# compare2 = []
# for eq in gb2:
#     symb1 = eq.free_symbols
#     if (Symbol("x3") in symb1 or Symbol("y3") in symb1) and Symbol("x1") not in symb1 and Symbol("y1") not in symb1 and Symbol("x2") not in symb1 and Symbol("y2") not in symb1:
#         compare2.append(eq)
# print(compare2)


# with open("construction_gb_3.json", "r") as f3:
#     gb_data = json.load(f3)
# variables = [symbols(var) for var in gb_data["variables"]]
# polynomials = [poly for poly in gb_data["basis"]]
# order = gb_data["order"]
# domain = gb_data["domain"]
# gb3 = groebner(polynomials, *variables, order=order, domain=domain)

# compare3 = []
# for eq in gb3:
#     symb1 = eq.free_symbols
#     if (Symbol("x4") in symb1 or Symbol("y4") in symb1) and Symbol("x1") not in symb1 and Symbol("y1") not in symb1 and Symbol("x2") not in symb1 and Symbol("y2") not in symb1 and Symbol("x3") not in symb1 and Symbol("y3") not in symb1:
#         compare3.append(eq)
# print(compare3)
