from sympy import solve, symbols, Symbol, Eq, init_printing, simplify
import string
from typing import Optional

from sympy.integrals.integrals import _
class Construction:
    def __init__(self, geometrical_objects):
        input_vars = []
        input_points = []
        for objec in geometrical_objects:
            if isinstance(objec, Line):
                input_points.append(objec.point1)
                input_points.append(objec.point2)
            elif isinstance(objec, Circle):
                input_points.append(objec.center)
                input_points.append(objec.point_on_circle)
            elif isinstance(objec, Point):
                input_points.append(objec)
            else:
                raise TypeError("Unsupported geometrical object type")
        for point in input_points:
            point.construction = self
            input_vars.append(point.x)
            input_vars.append(point.y)
            
        self.input_vars = input_vars
        self.used_vars = self.input_vars
        self.points = input_points
        self.system = []
        self.new_variable_counter = 0
    def get_system(self):
        return self.system
    def create_point(self):
        new_point = Point(self.get_new_var(), self.get_new_var(), self)
        self.points.append(new_point)
        return new_point
    def point(self, x, y):
        return Point(x,y, self)
    def point_on_object(self, object):
        return Point_on_object(self, object)
    def create_line(self, point1, point2):
        new_line = Line(point1, point2, self)
        return new_line
    def create_circle(self, center, point_on_circle):
        new_circle = Circle(center, point_on_circle, self)
        return new_circle
    
    def intersect(self, line_or_circle1, line_or_circle2):
        if isinstance(line_or_circle1, Line) and isinstance(line_or_circle2, Line):
            result = self.intersect_two_lines(line_or_circle1, line_or_circle2)
        elif isinstance(line_or_circle1, Circle) and isinstance(line_or_circle2, Circle):
            result = self.intersect_two_circles(line_or_circle1, line_or_circle2)
        elif isinstance(line_or_circle1, Line) and isinstance(line_or_circle2, Circle):
            result = self.intersect_line_circle(line_or_circle1, line_or_circle2)
        elif isinstance(line_or_circle1, Circle) and isinstance(line_or_circle2, Line):
            result = self.intersect_line_circle(line_or_circle2, line_or_circle1)
        else:
            print("Invalid geometrical object type!")
            result = None
        result = self.prevent_duplicate_points(result, line_or_circle1, line_or_circle2)
        for eq in result[0]:
            if simplify(eq) == True:
                eq = True
            self.add_equation(eq)
            print(eq)
        p1 = result[1]
        if len(result) == 3:
            p2 = result[2]
            print(f"--> coordinates ({p1.x},{p1.y}), ({p2.x},{p2.y}) of the two intersecting points")
        else:
            print(f"--> coordinates ({p1.x},{p1.y}) of the intersecting point")
        return result
    
    def intersect_two_lines(self, line1, line2):
        p = self.create_point()
        x = p.x
        y = p.y
        return [[line1.get_equation([x, y]), line2.get_equation([x, y])], p]
    
    def intersect_two_circles(self, circle1, circle2):
        p1 = self.create_point()
        x1 = p1.x
        y1 = p1.y
        p2 = self.create_point()
        x2 = p2.x
        y2 = p2.y
        D_squared = self.create_circle(circle1.center, circle2.center).squared_radius;
        return [[circle1.get_equation([x1, y1]), circle2.get_equation([x1, y1]), circle1.get_equation([x2, y2]), circle2.get_equation([x2, y2]), Eq(self.create_circle(self.point(x1, y1), self.point(x2, y2)).squared_radius, 4*circle1.squared_radius + ((circle1.squared_radius - circle2.squared_radius + D_squared)**2)/D_squared)], p1, p2]
   
    def intersect_line_circle(self, line, circle):
        p1 = self.create_point()
        x1 = p1.x
        y1 = p1.y
        p2 = self.create_point()
        x2 = p2.x
        y2 = p2.y
        d_squared  = (((line.point2.y - line.point1.y)*circle.center.x - (line.point2.x-line.point1.x)*circle.center.y + line.point2.x*line.point1.y - line.point1.x*line.point2.y)**2)/(self.create_circle(line.point1, line.point2).squared_radius)
        return [[line.get_equation([x1, y1]), circle.get_equation([x1, y1]), line.get_equation([x2, y2]), circle.get_equation([x2, y2]), Eq(self.create_circle(self.point(x1, y1), self.point(x2, y2)).squared_radius, 4*(circle.squared_radius - d_squared))], p1, p2]
    
        
    def coincide_points(self, point1, point2):
        # Checks if points eventually coincide
        if point1.x == point2.x and point1.y == point2.y:
            return True
        else:
            return False
        
    def prevent_duplicate_points(self, lst, object1, object2):
        # Prevents duplicate points
        equations = lst[0]
        p1 = lst[1]
        if len(lst) == 3: 
            p2 = lst[2]
            for point in self.points:
                if point == p1 or point == p2:
                    continue
                elif point.lie_on(object1) and point.lie_on(object2):
                    equations = [eq.subs({p2.x: point.x, p2.y: point.y}) for eq in equations]
                    self.used_vars.remove(p2.x)
                    self.used_vars.remove(p2.y)
                    self.new_variable_counter -= 2
                    self.points.remove(p2)
                    p2 = point
                    break
        else:
            for point in self.points:
                if point == p1:
                    continue
                elif point.lie_on(object1) and point.lie_on(object2):
                    equations = [eq.subs({p1.x: point.x, p1.y: point.y}) for eq in equations]
                    self.used_vars.remove(p1.x)
                    self.used_vars.remove(p1.y)
                    self.new_variable_counter -= 2
                    self.points.remove(p1)
                    p1 = point
                    break
        return [equations, p1, p2] if len(lst) == 3 else [equations, p1]

    def get_new_var(self):
        while True:
            self.new_variable_counter += 1  
            symb = Symbol(f'x{self.new_variable_counter}')
            if symb not in self.used_vars:
                self.used_vars.append(symb)
                return symb
    def add_equation(self, equation):
        self.system.append(equation)
            
    def get_arbitrary_point(self, object=None, contained_in_object: Optional[bool] = None, distance: Optional[float] =None):
        return AribitaryPoint(self, object,contained_in_object, distance)
    
class Point:
    def __init__(self, x, y, construction):
        self.x = x
        self.y = y
        self.construction = construction
    
    def x(self):
        return self.x

    def y(self):
        return self.y

    def lie_on(self, object):
        if simplify(object.get_equation([self.x, self.y])) == True:
            return True
        elif object.get_equation([self.x, self.y]) in self.construction.get_system():
            return True
        else:
            return False
        
    def to_str(self):
        return f"Point({self.x},{self.y})"
    
class AribitaryPoint(Point):
    def __init__(self, construction, gemetrical_object=None, contained_in_object: Optional[bool] = None, distance: Optional[float] = None):
        self.construction = construction
        self.x = construction.get_new_var()
        self.y = construction.get_new_var()
        self.construction.points.append(self)

        if gemetrical_object is not None:
            if contained_in_object:
                if isinstance(gemetrical_object, Line) or isinstance(gemetrical_object, Circle):
                    construction.add_equation(gemetrical_object.get_equation([self.x, self.y]))
                else:
                    raise TypeError("Unsupported geometrical object type")
            else:
                if distance is None:
                    construction.add_equation(gemetrical_object.get_equation([self.x, self.y]).lhs + 1)
                else:
                    if isinstance(gemetrical_object, Line):
                        construction.add_equation(
                            gemetrical_object.get_equation([self.x, self.y]).lhs ** 2,
                            (gemetrical_object.a ** 2 + gemetrical_object.b ** 2) * distance ** 2
                        )
                    elif isinstance(gemetrical_object, Circle):
                        construction.add_equation(
                            gemetrical_object.get_equation([self.x, self.y]).lhs ** 2,
                            gemetrical_object.get_squared_radius() + 2 * gemetrical_object.get_squared_radius() ** 0.5 * distance + distance ** 2
                        )
                    else:
                        raise TypeError("Unsupported geometrical object type")
                
class Point_on_object(Point):
    def __init__(self, construction, gemetrical_object):
        self.construction = construction
        self.x = construction.get_new_var()
        self.y = construction.get_new_var()
        self.construction.points.append(self)
        try:
            construction.add_equation(gemetrical_object.get_equation([self.x, self.y]))
        except: 
            raise TypeError("Unsupported geometrical object type")

class Line:
    def __init__(self, point1, point2, construction):
        self.point1 = point1
        self.point2 = point2
        if construction.coincide_points(point1, point2):
            print("The line is not determined as the two given points coincide.")
    def get_equation(self, variables=None):
        x1, y1 = self.point1.x, self.point1.y
        x2, y2 = self.point2.x, self.point2.y
        # Coefficients A, B, C for the line equation Ax + By + C = 0
        A = y1 - y2
        B = x2 - x1
        C = x1 * y2 - x2 * y1
        if variables == None:
            return Eq(A * Symbol('x') + B * Symbol('y') + C, 0)
        # Return the equation in the form Ax + By + C = 0
        return Eq(A * variables[0] + B * variables[1] + C, 0)
    def a(self):
        return self.point1.y - self.point2.y
    def b(self):
        return self.point2.x - self.point1.x
    def c(self):
        return self.point1.x * self.point2.y - self.point2.x * self.point1.y


class Circle:
    def __init__(self, center, point_on_circle, construction):
        self.center = center
        self.point_on_circle = point_on_circle
        if construction.coincide_points(center, point_on_circle):
            print("The circle coincides with its center")
        h, k = self.center.x, self.center.y
        x1, y1 = self.point_on_circle.x, self.point_on_circle.y
        self.squared_radius = (x1 - h)**2 + (y1 - k)**2

    def get_equation(self, variables=None):
        h, k = self.center.x, self.center.y
        x1, y1 = self.point_on_circle.x, self.point_on_circle.y

        # Calculate the radius using the distance formula
        r_squared = (x1 - h)**2 + (y1 - k)**2
        if variables == None:
            return Eq((Symbol('x') - h)**2 + (Symbol('y') - k)**2, r_squared)

        # Return the equation of the circle in the form (x-h)^2 + (y-k)^2 = r^2
        return Eq((variables[0] - h)**2 + (variables[1] - k)**2, r_squared)
    def get_squared_radius(self):
        h, k = self.center.x, self.center.y
        x1, y1 = self.point_on_circle.x, self.point_on_circle.y
        return (x1 - h)**2 + (y1 - k)**2