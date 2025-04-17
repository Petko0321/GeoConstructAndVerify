import json
from sympy import symbols, Symbol, sympify, groebner, fraction
from geocv import reduce_quadratics, simplify_expressions
import time

start_time = time.time()
with open("constructions\\geogebra\\construction3_grevlex.json", "r") as f1:
    gb_data = json.load(f1)
variables = [symbols(var) for var in gb_data["variables"]]
polynomials = [sympify(poly) for poly in gb_data["basis"]]
order = gb_data["order"]
domain = gb_data["domain"]
gb1 = groebner(polynomials, *variables, order=order, domain=domain)
# num_polynomials, denom_polynomials = simplify_expressions(gb1)
# print(num_polynomials)
# a, b, x, y = symbols('a b x y')
# num_polynomials = [x**2 - 2*a*x + a**2, y - b]
# num_polynomials = reduce_quadratics(num_polynomials, [a, b, x, y])
# num_polynomials = reduce_quadratics(num_polynomials, variables)
# print(num_polynomials)
# groebner_basis = [None]*len(num_polynomials)
# for i in range(len(num_polynomials)):
#     groebner_basis[i] = num_polynomials[i] / denom_polynomials[i]
# x1, y1, x2, y2, x3, y3, d6, d5, d4, d3, d2, d1 = variables
# reduced_gb1 = groebner(gb1, x1, y1, x2, y2, d6, x3, y3, d5, d4, order='lex', domain=domain)
# print(reduced_gb1)
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"Simplify elapsed time: {elapsed_time:.2f} seconds")

x1, y1, x2, y2, x3, y3, x4, y4, d7, d6, d5, d4, d3, d2, d1 = variables
reduced_gb = groebner(gb1, x1, y1, x2, y2, x3, y3, x4, y4, d6, d5, d7, d4, d3, d2, d1, order='lex', domain=domain)
print(reduced_gb)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Lex elapsed time: {elapsed_time:.2f} seconds")
gb_data3 = {
    "basis": [str(poly) for poly in reduced_gb],  # Запазване на полиномите като низове
    "variables": [str(var) for var in reduced_gb.gens],  # Променливите
    "order": str(reduced_gb.order),  # Реда (lex, grlex, grevlex)
    "domain": str(reduced_gb.domain),  # Полиномиалното поле (EX, ZZ, QQ и т.н.)
    "elapsed_time": float(elapsed_time)  # Време на изпълнение
}
with open("constructions\\geogebra\\construction3_lex1.json", "w") as f:
    json.dump(gb_data3, f, indent=4)
print("Грьобнеровата база е записана успешно!")

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
