from sympy import solve, symbols, Symbol, Eq, init_printing, simplify
import string

from sympy.integrals.integrals import _
class Construction:
    def __init__(self, geometrical_objects):
        input_vars = []
        input_points = []
        for objec in geometrical_objects:
            if type(objec) is Line:
                input_points.append(objec.point1)
                input_points.append(objec.point2)
            if type(objec) is Circle:
                input_points.append(objec.center)
                input_points.append(objec.point_on_circle)
            if type(objec) is Point:
                input_points.append(objec)
            else:
                TypeError
        for point in input_points:
            input_vars.append(point.x)
            input_vars.append(point.y)
            
        self.input_vars = input_vars
        self.used_vars = self.input_vars
        self.points = input_points
        self.system = []
        #self.variable_counter = len(self.used_vars)
        self.new_variable_counter = 0
    def get_system(self):
        return self.system
    def create_point(self):
        new_point = Point(self.get_new_var(), self.get_new_var(), self)
        self.points.append(new_point)
        return new_point
    def point(self, x, y):
        return Point(x,y, self)
    def create_line(self, point1, point2):
        return Line(point1, point2, self)
    def create_circle(self, center, point_on_circle):
        return Circle(center, point_on_circle, self)
    
    def intersect(self, line_or_circle1, line_or_circle2):
        if type(line_or_circle1) is type(line_or_circle2) is Line:
            result = self.intersect_two_lines(line_or_circle1, line_or_circle2)
        elif type(line_or_circle1) is type(line_or_circle2) is Circle:
            result = self.intersect_two_circles(line_or_circle1, line_or_circle2)
        elif type(line_or_circle1) is Line and type(line_or_circle2) is Circle:
            result = self.intersect_line_circle(line_or_circle1, line_or_circle2)
        elif type(line_or_circle1) is Circle and type(line_or_circle2) is Line:
            result = self.intersect_line_circle(line_or_circle2, line_or_circle1)
        else:
            print("Invalid argument!")
            result = None
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
        
    # def Get_new_var(self):
    #     alphabet = string.ascii_lowercase
    #     n = 1
    #     while True:  
    #         for i in range(len(alphabet) ** n):
    #             temp = ""
    #             num = i
    #             for _ in range(n):
    #                 temp = alphabet[num % len(alphabet)] + temp
    #                 num //= len(alphabet)
    #                 symb = Symbol(f'{temp}')
    #             if symb not in self.used_vars:
    #                 self.used_vars.append(symb)
    #                 return symb
    #         n += 1
            
    def get_new_var(self):
        while True:
            self.new_variable_counter += 1  
            symb = Symbol(f'x{self.new_variable_counter}')
            if symb not in self.used_vars:
                self.used_vars.append(symb)
                return symb
    def add_equation(self, equation):
        self.system.append(equation)
            
    def get_pairs(self):
        # Returns the pairs of solutions from previous intersection
        e1 = self.used_vars[-4]
        f1 = self.used_vars[-3]
        e2 = self.used_vars[-1]
        f2 = self.used_vars[-1]
        return [e1, f1, e2, f2]
    
class Point:
    def __init__(self, x, y, construction):
        self.x = x
        self.y = y
        self.construction = construction
    
    def x(self):
        return self.x

    def y(self):
        return self.y
 
    def lie_on_line(self, line):
        if str(simplify(line.get_equation([self.x, self.y]))) == 'True':
            return True
        return False
    


class Line:
    def __init__(self, point1, point2, construction):
        self.point1 = point1
        self.point2 = point2
        if construction.coincide_points(point1, point2):
            print("The line is not determined as the two given points coincide.")
        
    def get_equation(self, variables):
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


class Circle:
    def __init__(self, center, point_on_circle, construction):
        self.center = center
        self.point_on_circle = point_on_circle
        if construction.coincide_points(center, point_on_circle):
            print("The circle coincides with its center")
        h, k = self.center.x, self.center.y
        x1, y1 = self.point_on_circle.x, self.point_on_circle.y
        self.squared_radius = (x1 - h)**2 + (y1 - k)**2

    def get_equation(self, variables):
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
