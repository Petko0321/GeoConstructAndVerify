from sympy import symbols, simplify, groebner, solve, Expr
from basics import Line, Point
import time
# a1, b1, a2, b2, a3, b3 = symbols('a1, b1, a2, b2, a3, b3')
# x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7, x8, y8, x9, y9, d10, d9, d8, d7, d6, d5, d4, d3, d2, d1 = symbols('x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7, x8, y8, x9, y9, d10, d9, d8, d7, d6, d5, d4, d3, d2, d1')
# sys = [d1*((a1 - a2)**2 + (b1 - b2)**2) - 1, d2*((a1 - a3)**2 + (b1 - b3)**2) - 1, d3*((a2 - a3)**2 + (b2 - b3)**2) - 1, -(a1 - a3)**2 + (a1 - x1)**2 - (b1 - b3)**2 + (b1 - y1)**2, -(a2 - a3)**2 + (a2 - x1)**2 - (b2 - b3)**2 + (b2 - y1)**2, d4*((a3 - x1)**2 + (b3 - y1)**2) - 1, -a3*y1 + b3*x1 - x2*(b3 - y1) + y2*(a3 - x1), -(a3 - x1)**2 + (a3 - x2)**2 - (b3 - y1)**2 + (b3 - y2)**2, d5*((x1 - x2)**2 + (y1 - y2)**2) - 1]
# sys1 = sys + [-(x1 - x2)**2 + (-x2 + x3)**2 - (y1 - y2)**2 + (-y2 + y3)**2, (-x1 + x3)**2 - (x1 - x2)**2 + (-y1 + y3)**2 - (y1 - y2)**2, -(x1 - x2)**2 + (-x2 + x4)**2 - (y1 - y2)**2 + (-y2 + y4)**2, (-x1 + x4)**2 - (x1 - x2)**2 + (-y1 + y4)**2 - (y1 - y2)**2, d6*((x3 - x4)**2 + (y3 - y4)**2) - 1]
# sys = [eq.subs({a1:0,b1:0,a2:1,b2:1,a3:2,b3:0}) for eq in sys]
# st = time.time()
# print(solve(sys, x1, y1, x2, y2, d1, d2, d3, d4, d5))
# et = time.time()
# print(et-st)
# st = time.time()
# print(groebner(sys, x1, y1, x2, y2, d1, d2, d3, d4, d5, domain='EX', order='grevlex'))
# et = time.time()
# print(et-st)
# st = time.time()
# print(groebner(sys, x1, y1, x2, y2, d1, d2, d3, d4, d5, domain='EX', order='grlex'))
# et = time.time()
# print(et-st)
# st = time.time()
# print(groebner(sys, x1, y1, x2, y2, d1, d2, d3, d4, d5, domain='EX', order='lex'))
# et = time.time()
# print(et-st)
# st = time.time()
# print(solve(sys1, x1, y1, x2, y2, x3, y3, x4, y4, d1, d2, d3, d4, d5, d6))
# et = time.time()
# print(et-st)
# st = time.time()
# print(groebner(sys1, x1, y1, x2, y2, x3, y3, x4, y4, d1, d2, d3, d4, d5, d6, domain='EX', order='grevlex'))
# et = time.time()
# print(et-st)
# st = time.time()
# print(groebner(sys1, x1, y1, x2, y2, x3, y3, x4, y4, d1, d2, d3, d4, d5, d6, domain='EX', order='grlex'))
# et = time.time()
# print(et-st)
# st = time.time()
# print(groebner(sys1, x1, y1, x2, y2, x3, y3, x4, y4, d1, d2, d3, d4, d5, d6, domain='EX', order='lex'))
# et = time.time()
# print(et-st)


# s = [d1*((a1 - a2)**2 + (b1 - b2)**2) - 1,  d2*((a1 - a3)**2 + (b1 - b3)**2) - 1, d3*((a2 - a3)**2 + (b2 - b3)**2) - 1, -(a1 - a3)**2 + (a1 - x1)**2 - (b1 - b3)**2 + (b1 - y1)**2, -(a2 - a3)**2 + (a2 - x1)**2 - (b2 - b3)**2 + (b2 - y1)**2, d4*((a3 - x1)**2 + (b3 - y1)**2) - 1, -a3*y1 + b3*x1 - x2*(b3 - y1) + y2*(a3 - x1), -(a3 - x1)**2 + (a3 - x2)**2 - (b3 - y1)**2 + (b3 - y2)**2, d5*((x1 - x2)**2 + (y1 - y2)**2) - 1, -(a1 - a2)**2 + (a1 - x5)**2 - (b1 - b2)**2 + (b1 - y5)**2, -(a2 - a3)**2 + (a3 - x5)**2 - (b2 - b3)**2 + (b3 - y5)**2, d7*((a2 - x5)**2 + (b2 - y5)**2) - 1, -a2*y5 + b2*x5 - x6*(b2 - y5) + y6*(a2 - x5), -(a2 - x5)**2 + (a2 - x6)**2 - (b2 - y5)**2 + (b2 - y6)**2, d8*((x5 - x6)**2 + (y5 - y6)**2) - 1, 2*(x1-x2)*x9 +2*(y1-y2)*y9-x1**2+x2**2-y1**2+y2**2, 2*(x5-x6)*x9 +2*(y5-y6)*y9-x5**2+x6**2-y5**2+y6**2]
# st = time.time()
# print(groebner(s, x1, y1, x2, y2, x5, y5, x6, y6, x9, y9, d1, d2, d3, d4, d5, d7, d8, domain='EX', order='grevlex'))
# et = time.time()

# st = time.time()
# print(groebner(s, x1, y1, x2, y2, x5, y5, x6, y6, x9, y9, d1, d2, d3, d4, d5, d7, d8, domain='EX', order='grlex'))
# et = time.time()
# print(et-st)
# st = time.time()
# print(groebner(s, x1, y1, x2, y2, x5, y5, x6, y6, x9, y9, d1, d2, d3, d4, d5, d7, d8, domain='EX', order='lex'))
# et = time.time()
# print(et-st)
# print(et-st)
# st = time.time()
# print(solve(s, x1, y1, x2, y2, x5, y5, x6, y6, x9, y9, d1, d2, d3, d4, d5, d7, d8))
# et = time.time()
# print(et-st)


a1, b1, a2, b2, d1, d2, x1, y1, x2, y2 = symbols('a1, b1, a2, b2, d1, d2, x1, y1, x2, y2')
eq0 = d1*((a1-a2)**2+(b1-b2)**2)-1
eq1 = (x1-a1)**2+(y1-b1)**2-(a1-a2)**2-(b1-b2)**2
eq2 = (x1-a2)**2+(y1-b2)**2-(a1-a2)**2-(b1-b2)**2
eq3 = (x2-a1)**2+(y2-b1)**2-(a1-a2)**2-(b1-b2)**2
eq4 = (x2-a2)**2+(y2-b2)**2-(a1-a2)**2-(b1-b2)**2
# eq5 = (x1-x2)**2+(y1-y2)**2-3*(a1-a2)**2-3*(b1-b2)**2
eq5 = d2*((x1-x2)**2+(y1-y2)**2)-1
system = [eq0, eq1, eq2, eq3, eq4, eq5]
# system = [eq.subs({a1:0, b1:0, a2:2, b2:0}) for eq in system]
st = time.time()
print(system)
G = groebner(system, y1, x1, y2, x2, d2, d1, domain='EX', order='grevlex')
print(G)
et = time.time()
print(et-st)
st = time.time()
solution = solve(G, x1, y1, x2, y2, d2, d1)
print(solution)
x1, y1, x2, y2, d2, d1 = solution[0]
et = time.time()
line = Line(Point(x1,y1), Point(x2, y2))
print(line.get_equation())
x1, y1, x2, y2, d2, d1 = solution[1]
et = time.time()
line = Line(Point(x1,y1), Point(x2, y2))
print(line.get_equation())
print(et-st)