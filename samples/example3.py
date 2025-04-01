from geocv import Point, Construction, Circle
from geocv import circle_through_3_points, perpendicular_line
from sympy import symbols, groebner, solve
import time
# Example of construction the radical axis of two circles
# initial points
a1, b1, a2, b2, a3, b3, a4, b4 = symbols('a1 b1 a2 b2 a3 b3 a4 b4')
center1 = Point(a1, b1)
p1 = Point(a2, b2)
center2 = Point(a3, b3)
p2 = Point(a4, b4)
circle1 = Circle(center1, p1)
circle2 = Circle(center2, p2)
# construction
cons = Construction(circle1, circle2)
line1 = cons.create_line(center1, center2)
line2 = cons.create_line(p1, p2)
p3 = cons.get_arbitrary_point(line2, 1)
circle3 = circle_through_3_points(p1, p2, p3)
p4, p5 = cons.intersect(circle1, circle3)
p6, p7 = cons.intersect(circle2, circle3)
line2 = cons.create_line(p4, p5)
line3 = cons.create_line(p6, p7)
p8 = cons.intersect(line2, line3)
radical_axis = perpendicular_line(p8, line1, False)
cons.set_as_output(radical_axis)
print("The radical axis constructed")
print(f"Output object: {cons.output_object[0].equation}")
# visualize the points, the system, and variables
print("All points:")
for point in cons.points:
    print(point.to_str())
print("Construction system:")
print(cons.solution.get_system())
cons.solution.set_input_values(a1=0, b1=0, a2=2, b2=0, a3=5, b3=0, a4=5, b4=1)
gens = cons.get_generators()
start_time = time.time()
system = cons.solution.get_system()
print(system)
print(gens)
print("Proccesing")
gb = groebner(system, gens, domain='EX', order='grevlex')
print(gb)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")
for eq in gb:
    if (cons.solution.output_vars[0] in eq.free_symbols or cons.solution.output_vars[1] in eq.free_symbols):
        print(eq)
sol = solve(gb, cons.solution.output_vars)
print(sol)
cons.solution.values.update(sol)
sol = solve(gb, gens)
print(sol)
print(f"Output object: {cons.output_object[0].equation.subs(cons.solution.values)}")