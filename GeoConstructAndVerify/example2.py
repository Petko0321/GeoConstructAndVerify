from basics import Point, Construction, Vector
from utils import parallel_line, translate
from sympy import symbols, groebner
import time
# Example of separating a segment into n equal parts
# initial points - the vertices of the segment
a1, b1, a2, b2 = symbols('a1 b1 a2 b2')
p1 = Point(a1, b1, construction=None)
p2 = Point(a2, b2, construction=None)
# print("Enter n:")
# n = int(input())
n = 5
# construction
cons = Construction(p1, p2)
line1 = cons.create_line(p1, p2)
arib1 = cons.get_arbitrary_point(line1, False)
line2 = cons.create_line(p1, arib1)
current_center = arib1
current_point_on_circle = p1
points_on_line2 = []
# # without translate
# for i in range(1, n):
#     print(f"Step {i}")
#     points_on_line2.append(current_center)
#     cr = cons.create_circle(current_center, current_point_on_circle)
#     p3, _ = cons.intersect(cr, line2)
#     current_point_on_circle = current_center
#     current_center = p3
# print("End for loop")
# line3 = cons.create_line(current_center, p2)
# seperating_points = []
# for point in points_on_line2:
#     print(f"Step {point.to_str()}")
#     current_line = parallel_line(point, line3)
#     p = cons.intersect(current_line, line1)
#     seperating_points.append(p)
# with translate
current_vector = Vector(p1, arib1)
current_start = p1
current_end = arib1
for i in range(1, n):
    print(f"Step {i}")
    current_vector = translate(current_vector, current_end)
    current_start = current_vector.starting_point
    current_end = current_vector.ending_point
    points_on_line2.append(current_start)
line3 = cons.create_line(p2, current_end)
print("End for loop")
seperating_points = []
seperating_points[0] = cons.intersect(line1, parallel_line(points_on_line2[0], line3))
current_vector = Vector(p1, seperating_points[0])
for i in range(1, n-1):
    current_vector = translate(current_vector, current_end)
    current_start = current_vector.starting_point
    current_end = current_vector.ending_point
    points_on_line2.append(current_start)
    
    
print(f"The points which seperate the segment into {n} equal parts are:")
for point in seperating_points:
    print(point.to_str())
print("finished")
# visualize the points, the system, and variables
print("All points:")
for point in cons.points:
    print(point.to_str())
print("Construction system:")
print(cons.solution.get_system())
print(cons.all_vars)
# perform calculations
cons.set_as_output(seperating_points)
gens = cons.get_generators()

cons.solution.set_input_values(a1=0, b1=0, a2=5, b2=0)
start_time = time.time()
system = cons.solution.get_system()
print(system)
print("Proccesing")
gb = groebner(system, gens, domain='EX', order='grevlex' )
print(gb)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")
# End example