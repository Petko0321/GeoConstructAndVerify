
import math
from sympy import solve, symbols, Symbol, Eq, init_printing, simplify
from basics import AribitaryPoint, Point, Construction

def perpendicular_bisector(point1, point2, construction, only_line=False):
    # Returns  equations derived form the construction, the intersecting points which determine
    # the perpendicular bisector and the perpendicular bisector as Line object
    c1 = construction.create_circle(point1, point2)
    c2 = construction.create_circle(point2, point1)
    equations, p1, p2 = construction.intersect(c1, c2)
    perpendicular_bisector = construction.create_line(p1, p2)
    if only_line:
        return perpendicular_bisector
    else:
        return [equations, p1, p2, perpendicular_bisector]
    
    # If we wanted to return the equation of the perpendicular bisector, we'd used this:
    # intersecting_points = solve(equations,construction.vars)
    # l2 = Line(Point(intersecting_points[0][0], intersecting_points[0][1]), Point(intersecting_points[1][0], intersecting_points[1][1]))
    # return simplify(l2.get_equation([x, y]))
    # But it's too slow
    

def perpendicular_line(point, line, point_is_on_line, construction, only_line=False):
    # Returns  equations derived form the construction, the intersecting points which determine
    # the perpendicular line and the perpendicular line as Line object
    # Two possible routes depending upon whether the point lies on the line
    all_equations = []
    if point_is_on_line:
        c1 = construction.create_circle(point, line.point1)
        equations, p1, p2 = construction.intersect(c1, line)
        for eq in equations:
            all_equations.append(eq)
        equations, p1, p2, perpendicular_line = perpendicular_bisector(p1, p2, construction)
        for eq in equations:
            all_equations.append(eq)
    else:
        c1 = construction.create_circle(line.point1, point)
        c2 = construction.create_circle(line.point2, point)
        equations, p1, p2 = construction.intersect(c1, c2)
        for eq in equations:
            all_equations.append(eq)
        perpendicular_line = construction.create_line(p1, p2)
    if only_line:
        return perpendicular_line
    else:
        return [all_equations, p1, p2, perpendicular_line]

def parallel_line(point, line, construction, only_line=False):
    # Construct a parallel line through point not lying on a given line
    # Returns  equations derived form the construction, the intersecting points which determine
    # the parallel line and the parallel line as Line object
    all_equations = []
    equations, _, _, perpendicular_line1 = perpendicular_line(point, line, False, construction)
    for eq in equations:
       all_equations.append(eq)
    # point_in_on_line is given false
    equations, p1, p2, parallel_line = perpendicular_line(point, perpendicular_line1, True, construction)
    for eq in equations:
       all_equations.append(eq)
    # point_is_on_line is obviously true 
    if only_line:
        return parallel_line
    else:
        return [all_equations, p1, p2, parallel_line]


# class Segment:
#     def __init__(self, point1, point2):
#         self.point1 = point1
#         self.point2 = point2
#     def length(self):
#         return math.sqrt((self.point1.x - self.point2.x)**2 + (self.point1.y-self.point2.y)**2)

class Vector:
    def __init__(self, starting_point, ending_point):
        self.starting_point = starting_point
        self.ending_point = ending_point
    def length(self):
        return ((self.starting_point.x - self.ending_point.x)**2 + (self.starting_point.y-self.ending_point.y)**2)**(1/2)
    
def translate_vector(vector, point, construction, only_vector=False):
    # Translate a vector method (not working if all points on the same line)
    # Returns  equations derived form the construction, the fourth vertex of 
    # the parallelogram and the wanted vector
   p1 = vector.starting_point
   p2 = vector.ending_point
   p3 = point
   line1 = construction.create_line(p1, p2)
   line2 = construction.create_line(p1, p3)
   all_equations = []
   equations, _, _, line3 = parallel_line(p3, line1, construction)
   for eq in equations:
       all_equations.append(eq)
   equations, _, _, line4 = parallel_line(p2, line2, construction)
   for eq in equations:
       all_equations.append(eq)
   equations, p = construction.intersect(line3, line4)
   for eq in equations:
            all_equations.append(eq)
   wanted_vector = Vector(p3, p)
   if only_vector:
       return wanted_vector
   else:
        return [all_equations, p, wanted_vector]

def translate(vector, point, construction, only_vector=False):
        # Translate a vector method (enhanced)
        # Returns  equations derived form the construction, the fourth vertex of 
        # the parallelogram and the wanted vector
    p1 = vector.starting_point
    p2 = vector.ending_point
    p3 = point
    line1 = construction.create_line(p1, p2)
    if p3.lie_on(line1):
        print("The point lies on the line")
        all_equations = []
        equations, _, v1 = translate_vector(vector, construction.get_arbitrary_point(line1, False), construction)
        for eq in equations:
            all_equations.append(eq)
        equations, p, wanted_vector = translate_vector(v1, point, construction)
        for eq in equations:
            all_equations.append(eq)
        result = [all_equations, p, wanted_vector]
    else:
        print("The point does not lie on the line")
        result = translate_vector(vector, point, construction)
    #print(f"The wanted vectror is from ({wanted_vector.starting_point.x}, {wanted_vector.starting_point.y}) to ({wanted_vector.ending_point.x}, {wanted_vector.ending_point.y})")
    if only_vector:
        return result[2]
    return result
def circle_through_3_points(point1, point2, point3, construction, only_circle=False):
    # Construct a circle through 3 points
    # Returns  equations derived form the construction, the center of the circle and the radius
    # of the circle
    all_equations = []
    equations, _, _, perpendicular_bisector1 = perpendicular_bisector(point1, point2, construction)
    for eq in equations:
        all_equations.append(eq)
    equations, _, _, perpendicular_bisector2 = perpendicular_bisector(point2, point3, construction)
    for eq in equations:
        all_equations.append(eq)
    equations, center = construction.intersect(perpendicular_bisector1, perpendicular_bisector2)
    for eq in equations:
        all_equations.append(eq)
    circle = construction.create_circle(center, point1)
    if only_circle:
        return circle
    else:
        return [all_equations, center, circle]
