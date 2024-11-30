from sympy import solve, symbols, Symbol, Eq, init_printing, simplify
class Construction:
    def __init__(self, vars):
        for i in range(len(vars)):
            vars[i] = Symbol(vars[i])
        self.vars = vars
        self.left_vars = vars
    def vars(self):
        return self.vars
    def left_vars(self):
        return self.left_vars
    def system(self):
        return self.system
    
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def x(self):
        return self.x

    def y(self):
        return self.y
 
    def lie_on_line(self, line):
        if str(simplify(line.get_equation([self.x, self.y]))) == 'True':
            return True
        return False


class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        if coincide_points(point1, point2):
            print("The line is not determined as the two given points coincide.")

    def get_equation(self, variables):
        x, y = variables[0], variables[1]
        x1, y1 = self.point1.x, self.point1.y
        x2, y2 = self.point2.x, self.point2.y

        # Coefficients A, B, C for the line equation Ax + By + C = 0
        A = y1 - y2
        B = x2 - x1
        C = x1 * y2 - x2 * y1

        # Return the equation in the form Ax + By + C = 0
        return Eq(A * x + B * y + C, 0)


class Circle:
    def __init__(self, center, point_on_circle):
        self.center = center
        self.point_on_circle = point_on_circle
        if coincide_points(center, point_on_circle):
            print("The circle coincides with its center")

    def get_equation(self, variables):
        h, k = self.center.x, self.center.y
        x1, y1 = self.point_on_circle.x, self.point_on_circle.y

        # Calculate the radius using the distance formula
        r_squared = (x1 - h)**2 + (y1 - k)**2

        # Return the equation of the circle in the form (x-h)^2 + (y-k)^2 = r^2
        return Eq((variables[0] - h)**2 + (variables[1] - k)**2, r_squared)

#Returns the intersecting points symbolically
def intersect(line_or_circle1, line_or_circle2, variables):
    if type(line_or_circle1) is type(line_or_circle2) is Line:
        result = intersect_two_lines(line_or_circle1, line_or_circle2, variables)
    elif type(line_or_circle1) is type(line_or_circle2) is Circle:
        result = intersect_two_circles(line_or_circle1, line_or_circle2, variables)
    elif type(line_or_circle1) is Line and type(line_or_circle2) is Circle:
        result = intersect_line_circle(line_or_circle1, line_or_circle2, variables)
    elif type(line_or_circle1) is Circle and type(line_or_circle2) is Line:
        result = intersect_line_circle(line_or_circle2, line_or_circle1, variables)
    else:
        print("Invalid argument!")
        result = None
    return result

def intersect_two_lines(line1, line2, variables):
    # Solve for the intersection point symbolically
    x = variables[0]
    y = variables[1]
    # variables.remove(x)
    # variables.remove(y)
    return [line1.get_equation([x, y]), line2.get_equation([x, y])]

def intersect_two_circles(circle1, circle2, variables):
# Solve for the intersection point symbolically
    x = variables[0]
    y = variables[1]
    # variables.remove(x)
    # variables.remove(y)
    return [circle1.get_equation([x, y]), circle2.get_equation([x, y])]

def intersect_line_circle(line, circle, variables):
# Solve for the intersection point symbolically
    x = variables[0]
    y = variables[1]
    # variables.remove(x)
    # variables.remove(y)
    return [line.get_equation([x, y]), circle.get_equation([x, y])]

# Checks if points eventually coincide
def coincide_points(point1, point2):
    if point1.x == point2.x and point1.y == point2.y:
        return True
    else:
        return False
    
x, y = symbols('x y')
