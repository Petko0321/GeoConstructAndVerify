
import math
import string
from sympy import solve, symbols, Symbol, Eq, init_printing, simplify
from basics import Line, Circle, intersect, Point, Construction,  x, y

def perpendicular_bisector(point1, point2, variables, construction):
    # Returns the equations which have their roots the coordinates of the intersecting
    # points which determine the perpendicular bisector
    # if type(variables)== Construction:
    #     variables = variables.vars
    c1 = Circle(point1, point2)
    c2 = Circle(point2, point1)
    equations = intersect(c1, c2, variables)
    for eq in equations:
        print(eq)
    print(f"--> coordinates ({variables[0]}1,{variables[1]}1), ({variables[0]}2,{variables[1]}2) of the two intersecting points")
    return equations
    
    # If we wanted to return the equation of the perpendicular bisector, we'd used this:
    # intersecting_points = solve(equations,construction.vars)
    # l2 = Line(Point(intersecting_points[0][0], intersecting_points[0][1]), Point(intersecting_points[1][0], intersecting_points[1][1]))
    # return simplify(l2.get_equation([x, y]))
    # But it's too slow
    

def perpendicular_line(point, line, point_is_on_line, variables, construction):
    # Returns the equations used to construct a perpendicular line
    # Two possible routes depending on if the point lies on the line
    all_equations = []
    if point_is_on_line:
        e = construction.vars[0]
        f = construction.vars[1]
        e1 = Symbol(f'{construction.vars[0]}1')
        e2 = Symbol(f'{construction.vars[0]}2')
        f1 = Symbol(f'{construction.vars[1]}1')
        f2 = Symbol(f'{construction.vars[1]}2')
        c1 = Circle(point, line.point1)
        equations = intersect(c1, line, [e, f])
        for eq in equations:
            print(eq)
            all_equations.append(eq)
        print(f"--> coordinates ({e}1,{f}1), ({e}2,{f}2) of the two intersecting points")
        construction.left_vars.remove(e)
        construction.left_vars.remove(f)
        h = construction.vars[0]
        k = construction.vars[1]
        equations = perpendicular_bisector(Point(e1, f1), Point(e2, f2), [h, k], construction)
        all_equations.append(equations[0])
        all_equations.append(equations[1])
        print(f"The points ({h}1,{k}1) and ({h}2,{k}2) determine the wanted line")
        construction.left_vars.remove(h)
        construction.left_vars.remove(k)
    else:
        h = construction.vars[0]
        k = construction.vars[1]
        c1 = Circle(line.point1, point)
        c2 = Circle(line.point2, point)
        equations = intersect(c1, c2, [h, k])
        for eq in equations:
            print(eq)
            all_equations.append(eq)
        print(f"--> coordinates ({h}1,{k}1), ({h}2,{k}2) of the two intersecting points")
        print(f"The points ({h}1,{k}1) and ({h}2,{k}2) determine the wanted line")
        construction.left_vars.remove(h)
        construction.left_vars.remove(k)
    return all_equations

def parallel_line(point, line, variables, construction):
    # Construct a parallel line through point not lying on a given line
    system = []
    e1 = Symbol(f'{construction.vars[0]}1')
    e2 = Symbol(f'{construction.vars[0]}2')
    f1 = Symbol(f'{construction.vars[1]}1')
    f2 = Symbol(f'{construction.vars[1]}2')
    equations = perpendicular_line(point, Line(line.point1, line.point2), False, construction.vars, construction)
    for eq in equations:
       system.append(eq)
    # point_in_on_line is given false
    l1 = Line(Point(e1, f1), Point(e2, f2))
    equations = perpendicular_line(p3, l1, True, construction.vars, construction)
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
    
def Translate(vector, point, variables, construction):
    # Translate a vector method (not enhanced)
   p1 = vector.starting_point
   p2 = vector.ending_point
   p3 = point
   line1 = Line(p1, p2)
   line2 = Line(p1, p3)
   system = []
   equations = parallel_line(p3, line1, construction.vars, construction)
   for eq in equations:
       system.append(eq)
   index = len(construction.vars) - len(construction.left_vars)
   line3 = Line(Point(Symbol(f'{construction.vars[index]}1'), Symbol(f'{construction.vars[index+1]}1')), Point(Symbol(f'{construction.vars[index]}2'), Symbol(f'{construction.vars[index+1]}2')))
   print(line3.get_equation([x, y]))
   equations = parallel_line(p2, line2, construction.vars, construction)
   for eq in equations:
       system.append(eq)
   index = len(construction.vars) - len(construction.left_vars)
   line4 = Line(Point(Symbol(f'{construction.vars[index]}1'), Symbol(f'{construction.vars[index+1]}1')), Point(Symbol(f'{construction.vars[index]}2'), Symbol(f'{construction.vars[index+1]}2')))
   equations = intersect(line3, line4, [x, y])
   for eq in equations:
            print(eq)
            system.append(eq)
   print(f"--> coordinates (x, y) of the intersecting point")
   print("The wanted line segment is from p3(c3, d3) to X(x, y)")
   return system

def Generate_new_vars(number_of_vars, vars_to_skip):
    alphabet = string.ascii_lowercase
    result = []
    n = 1

    while len(result) < number_of_vars:
        for i in range(len(alphabet) ** n):
            temp = ""
            num = i
            for _ in range(n):
                temp = alphabet[num % len(alphabet)] + temp
                num //= len(alphabet)
            if temp not in vars_to_skip:
                 result.append(temp)
            if len(result) == number_of_vars:
                break
        n += 1
    # for i in result:
    #     i = Symbol(f'{i}')

    return result

# Translate a vector 
c1, d1, c2, d2, c3, d3 = symbols('c1 d1 c2 d2 c3 d3')
# a, b, e, f, g, h, i, j, k, l, m, n, o, p, v, u, w, z = symbols('a b e f g h i j k l m n o p v u w z')
# all_variables = [a, b, e, f, g, h, i, j, k, l, m, n, o, p, v, u, w, z]
# vars = [a, b, e, f, g, h, i, j, k, l, m, n, o, p, v, u, w, z]
vars = Generate_new_vars(50, ["c", "d"])
construction = Construction(vars)
for i in vars:
    print(i)
p1 = Point(c1, d1)
p2 = Point(c2, d2)
p3 = Point(c3, d3)
Translate(Vector(p1,p2),p3, construction.vars, construction)