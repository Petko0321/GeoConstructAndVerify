import json
from sympy import symbols, Symbol, sympify, groebner

# with open("construction_gb_1.json", "r") as f1:
#     gb_data = json.load(f1)
# variables = [symbols(var) for var in gb_data["variables"]]
# polynomials = [sympify(poly) for poly in gb_data["basis"]]
# order = gb_data["order"]
# domain = gb_data["domain"]
# gb1 = groebner(polynomials, *variables, order=order, domain=domain)

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


with open("construction_gb_3.json", "r") as f3:
    gb_data = json.load(f3)
variables = [symbols(var) for var in gb_data["variables"]]
polynomials = [poly for poly in gb_data["basis"]]
order = gb_data["order"]
domain = gb_data["domain"]
gb3 = groebner(polynomials, *variables, order=order, domain=domain)

compare3 = []
for eq in gb3:
    symb1 = eq.free_symbols
    if (Symbol("x4") in symb1 or Symbol("y4") in symb1) and Symbol("x1") not in symb1 and Symbol("y1") not in symb1 and Symbol("x2") not in symb1 and Symbol("y2") not in symb1 and Symbol("x3") not in symb1 and Symbol("y3") not in symb1:
        compare3.append(eq)
print(compare3)

