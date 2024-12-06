
import math
import string
from sympy import solve, symbols, Symbol, Eq, init_printing, simplify
from basics import Point, Construction

def perpendicular_bisector(point1, point2, construction):
    # Returns the equations which have their roots the coordinates of the intersecting
    # points which determine the perpendicular bisector
    # if type(variables)== Construction:
    #     variables = variables.vars
    c1 = construction.create_circle(point1, point2)
    c2 = construction.create_circle(point2, point1)
    equations = construction.intersect(c1, c2)
    for eq in equations:
        print(eq)
    print(f"--> coordinates ({construction.used_vars[-2]}1,{construction.used_vars[-1]}1), ({construction.used_vars[-2]}2,{construction.used_vars[-1]}2) of the two intersecting points")
    return equations
    
    # If we wanted to return the equation of the perpendicular bisector, we'd used this:
    # intersecting_points = solve(equations,construction.vars)
    # l2 = Line(Point(intersecting_points[0][0], intersecting_points[0][1]), Point(intersecting_points[1][0], intersecting_points[1][1]))
    # return simplify(l2.get_equation([x, y]))
    # But it's too slow
    

def perpendicular_line(point, line, point_is_on_line, construction):
    # Returns the equations used to construct a perpendicular line
    # Two possible routes depending on if the point lies on the line
    all_equations = []
    if point_is_on_line:
        c1 = construction.create_circle(point, line.point1)
        equations = construction.intersect(c1, line)
        for eq in equations:
            print(eq)
            all_equations.append(eq)
        e = construction.used_vars[-2]
        f = construction.used_vars[-1]
        e1 = Symbol(f'{e}1')
        e2 = Symbol(f'{e}2')
        f1 = Symbol(f'{f}1')
        f2 = Symbol(f'{f}2')
        print(f"--> coordinates ({e}1,{f}1), ({e}2,{f}2) of the two intersecting points")
        equations = perpendicular_bisector(construction.create_point(e1, f1), construction.create_point(e2, f2), construction)
        for eq in equations:
            all_equations.append(eq)
        h = construction.used_vars[-2]
        k = construction.used_vars[-1]
        print(f"The points ({h}1,{k}1) and ({h}2,{k}2) determine the wanted line")
        # construction.used_vars.append(h)
        # construction.used_vars.append(k)
    else:
        c1 = construction.create_circle(line.point1, point)
        c2 = construction.create_circle(line.point2, point)
        equations = construction.intersect(c1, c2)
        h = construction.used_vars[-2]
        k = construction.used_vars[-1]
        for eq in equations:
            print(eq)
            all_equations.append(eq)
        print(f"--> coordinates ({h}1,{k}1), ({h}2,{k}2) of the two intersecting points")
        print(f"The points ({h}1,{k}1) and ({h}2,{k}2) determine the wanted line")
    return all_equations

def parallel_line(point, line, construction):
    # Construct a parallel line through point not lying on a given line
    system = []
    # e = construction.Get_new_var()
    # f = construction.Get_new_var()
    # e1 = Symbol(f'{e}1')
    # e2 = Symbol(f'{e}2')
    # f1 = Symbol(f'{f}1')
    # f2 = Symbol(f'{f}2')
    equations = perpendicular_line(point, construction.create_line(line.point1, line.point2), False, construction)
    for eq in equations:
       system.append(eq)
    # point_in_on_line is given false
    e = construction.used_vars[-2]
    f = construction.used_vars[-1]
    e1 = Symbol(f'{e}1')
    e2 = Symbol(f'{e}2')
    f1 = Symbol(f'{f}1')
    f2 = Symbol(f'{f}2')
    l1 = construction.create_line(construction.create_point(e1, f1), construction.create_point(e2, f2))
    equations = perpendicular_line(p3, l1, True, construction)
    for eq in equations:
       system.append(eq)
    # point_is_on_line is obviously true 
    # Has to be considered how to automatize this using a function
    return system


class Segment:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
    def length(self):
        return math.sqrt((self.point1.x - self.point2.x)**2 + (self.point1.y-self.point2.y)**2)

class Vector:
    def __init__(self, starting_point, ending_point):
        self.starting_point = starting_point
        self.ending_point = ending_point
    def length(self):
        return math.sqrt((self.starting_point.x - self.ending_point.x)**2 + (self.starting_point.y-self.ending_point.y)**2)
    
def Translate(vector, point, construction):
    # Translate a vector method (not enhanced)
   p1 = vector.starting_point
   p2 = vector.ending_point
   p3 = point
   line1 = construction.create_line(p1, p2)
   line2 = construction.create_line(p1, p3)
   system = []
   equations = parallel_line(p3, line1, construction)
   for eq in equations:
       system.append(eq)
   line3 = construction.create_line(construction.create_point(Symbol(f'{construction.used_vars[-2]}1'), Symbol(f'{construction.used_vars[-1]}1')), construction.create_point(Symbol(f'{construction.used_vars[-2]}2'), Symbol(f'{construction.used_vars[-1]}2')))
   #print(line3.get_equation(variables=None))
   equations = parallel_line(p2, line2, construction)
   for eq in equations:
       system.append(eq)
   line4 = construction.create_line(construction.create_point(Symbol(f'{construction.used_vars[-2]}1'), Symbol(f'{construction.used_vars[-1]}1')), construction.create_point(Symbol(f'{construction.used_vars[-2]}2'), Symbol(f'{construction.used_vars[-1]}2')))
   equations = construction.intersect(line3, line4)
   for eq in equations:
            print(eq)
            system.append(eq)
   print(f"--> coordinates (x, y) of the intersecting point")
   print("The wanted line segment is from p3(c3, d3) to X(x, y)")
   return system

# a, b, e, f, g, h, i, j, k, l, m, n, o, p, v, u, w, z = symbols('a b e f g h i j k l m n o p v u w z')
# all_variables = [a, b, e, f, g, h, i, j, k, l, m, n, o, p, v, u, w, z]
# vars = [a, b, e, f, g, h, i, j, k, l, m, n, o, p, v, u, w, z]

# Translate a vector 
c1, d1, c2, d2, c3, d3 = symbols('c1 d1 c2 d2 c3 d3')
p1 = Point(c1, d1, construction=None)
p2 = Point(c2, d2, construction=None)
p3 = Point(c3, d3, construction=None)
cons = Construction([p1, p2, p3])
Translate(Vector(p1, p2), p3, cons)
print(cons.used_vars)