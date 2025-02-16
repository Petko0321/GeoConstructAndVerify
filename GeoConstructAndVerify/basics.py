from sympy import solve, symbols, Symbol, Eq, init_printing, simplify, ring, RR, groebner, fraction, Mul
from sympy.polys.orderings import monomial_key
import string
from typing import Optional

from sympy.integrals.integrals import _


class Solution:
    def __init__(self, construction, output_vars, input_vars=[]):
        self.input_vars = input_vars
        self.output_vars = output_vars
        self.construction = construction
        system_eqs = construction.get_system()
        self.system = []
        for eq in system_eqs:
            if eq == True:
                continue
            if not isinstance(eq, Eq):
                print(f"Here: {eq}")
            expr = eq.lhs - eq.rhs
            numerator, denominator = expr.as_numer_denom()
            expr = simplify(Mul(numerator, denominator, evaluate=False))
            self.system.append(expr)
            self.all_vars = []
            for v in construction.all_vars:
                if isinstance(v, Symbol):
                    self.all_vars.append(v)
        self.synthetic_vars = [
            var for var in self.all_vars if var not in input_vars and var not in output_vars]
        # ringg = ring(self.all_vars, RR)[0]
        order = monomial_key(self.custom_order)
        self.reduced_groebner_basis = groebner(
            self.system, self.all_vars, method="buchberger", order="grlex")

    def custom_order(self, monomial):
        # Define the custom monomial order
        synthetic_part = monomial[:len(self.synthetic_vars)]
        output_part = monomial[len(self.synthetic_vars):len(
            self.synthetic_vars) + len(self.output_vars)]
        input_part = monomial[len(self.synthetic_vars) +
                              len(self.output_vars):]

        # Priority order: Synthetic > Output > Input
        return (tuple(-exp for exp in synthetic_part),
                tuple(-exp for exp in output_part),
                tuple(-exp for exp in input_part))


class Construction:
    def __init__(self, *geometrical_objects, input_equations=None):
        input_vars = []
        input_points = []
        self.system = []
        self.distances = []
        for objec in geometrical_objects:
            if isinstance(objec, Line):
                input_points.append(objec.point1)
                input_points.append(objec.point2)
            elif isinstance(objec, Circle):
                input_points.append(objec.center)
                input_points.append(objec.point_on_circle)
            elif isinstance(objec, Point):
                input_points.append(objec)
            elif isinstance(objec, Polygon):
                for point in objec.points:
                    input_points.append(point)
            else:
                raise ValueError("Unsupported geometrical object type")
        for point in input_points:
            point.construction = self
            input_vars.append(point.x)
            input_vars.append(point.y)

        self.input_vars = input_vars
        self.all_vars = self.input_vars
        self.points = input_points
        for i in range(len(input_points)):
            for j in range(i + 1, len(input_points)):
                point1 = input_points[i]
                point2 = input_points[j]
                self.add_equation(Eq(((point1.x-point2.x)**2+(point1.y-point2.y)**2)*self.get_new_d(point1, point2), 1))
        self.input_eqs = []
        self.input_eqs = [eq for eq in self.system]
        self.input_vars = input_vars
        self.all_vars = self.input_vars
        self.points = input_points
        if input_equations != None:
            for eq in input_equations:
                self.add_equation(eq)
        self.new_variable_counter = 0
        self.optimization_equations = []

    def get_system(self):
        return self.system

    def create_point(self):
        new_point = Point(self.get_new_var(), self.get_new_var(), self)
        self.points.append(new_point)
        return new_point

    def point(self, x, y):
        return Point(x, y, self)

    def get_arbitrary_point(self, object=None, distance: Optional[float] = None):
        return AribitaryPoint(self, object, distance)

    def point_on_object(self, object):
        return AribitaryPoint(self, object)

    def create_line(self, point1, point2):
        new_line = Line(point1, point2, self)
        return new_line

    def create_circle(self, center, point_on_circle):
        new_circle = Circle(center, point_on_circle, self)
        return new_circle

    def intersect(self, line_or_circle1, line_or_circle2, only_points: bool = True, point_coordinator=None):
        self.optimized_eqs = []
        if isinstance(line_or_circle1, Line) and isinstance(line_or_circle2, Line):
            result = self.intersect_two_lines(line_or_circle1, line_or_circle2)
        elif isinstance(line_or_circle1, Circle) and isinstance(line_or_circle2, Circle):
            result = self.intersect_two_circles(
                line_or_circle1, line_or_circle2)
        elif isinstance(line_or_circle1, Line) and isinstance(line_or_circle2, Circle):
            result = self.intersect_line_circle(
                line_or_circle1, line_or_circle2, point_coordinator)
        elif isinstance(line_or_circle1, Circle) and isinstance(line_or_circle2, Line):
            result = self.intersect_line_circle(
                line_or_circle2, line_or_circle1, point_coordinator)
        else:
            raise ValueError("Invalid geometrical object type!")
            result = None
        result = self.prevent_duplicate_points(result, line_or_circle1, line_or_circle2)
        
        duplicates = result.pop(-1)
        if len(duplicates) != 0:
            for duplicate in duplicates:
                old, new = duplicate  
                for eq in self.optimized_eqs:
                    after_subs = simplify(eq.subs({old.x: new.x, old.y: new.y}))
                    if after_subs != 0:
                        self.optimization_equations.append(after_subs)
        else:
            self.optimization_equations.extend(self.optimized_eqs)

        for eq in result[0]:
            if simplify(eq) == True or eq in self.system:
                eq = True
            self.add_equation(eq)
            print(eq)
        p1 = result[1]
        if len(result) == 3:
            p2 = result[2]
            if only_points:
                result.remove(result[0])
            print(f"--> coordinates ({p1.x},{p1.y}), ({p2.x},{p2.y}) of the two intersecting points")
        else:
            if only_points:
                result = result[1]
            print(f"--> coordinates ({p1.x},{p1.y}) of the intersecting point")
        return result

    def intersect_two_lines(self, line1, line2):
        p = self.create_point()
        x = p.x
        y = p.y
        a1, b1, c1 = line1.a(), line1.b(), line1.c()
        a2, b2, c2 = line2.a(), line2.b(), line2.c()
        self.optimized_eqs.extend([x*(a1*b2 - a2*b1) - (b1*c2 - b2*c1), y*(a1*b2 - a2*b1) - (a2*c1 - a1*c2)])
        return [[line1.get_equation([x, y]), line2.get_equation([x, y])], p]

    def intersect_two_circles(self, circle1, circle2):
        p1 = self.create_point()
        x1 = p1.x
        y1 = p1.y
        p2 = self.create_point()
        x2 = p2.x
        y2 = p2.y
        m1, n1 = circle1.center.x, circle1.center.y
        m2, n2 = circle2.center.x, circle2.center.y
        r1_sqr = circle1.squared_radius
        r2_sqr = circle2.squared_radius
        d = self.get_new_d(p1, p2)
        self.optimized_eqs.extend([(x1*(m1 - m2)*(m1**3 - 3*m1**2*m2 + 3*m1*m2**2 + m1*n1**2 - 2*m1*n1*n2 + m1*n2**2 - m2**3 - m2*n1**2 + 2*m2*n1*n2 - m2*n2**2) - y2*(n1 - n2)*(m1**3 - 3*m1**2*m2 + 3*m1*m2**2 + m1*n1**2 - 2*m1*n1*n2 + m1*n2**2 - m2**3 - m2*n1**2 + 2*m2*n1*n2 - m2*n2**2) + (m1 - m2)*(-m1**4 + 2*m1**3*m2 + 2*m1**2*n1*n2 - 2*m1**2*n2**2 + m1**2*r1_sqr - m1**2*r2_sqr - 2*m1*m2**3 - 2*m1*m2*n1**2 + 2*m1*m2*n2**2 - 2*m1*m2*r1_sqr + 2*m1*m2*r2_sqr + m2**4 + 2*m2**2*n1**2 - 2*m2**2*n1*n2 + m2**2*r1_sqr - m2**2*r2_sqr + n1**4 - 2*n1**3*n2 - n1**2*r1_sqr + n1**2*r2_sqr + 2*n1*n2**3 + 2*n1*n2*r1_sqr - 2*n1*n2*r2_sqr - n2**4 - n2**2*r1_sqr + n2**2*r2_sqr)/2), (-m1**2*n1 - m1**2*n2 + 2*m1*m2*n1 + 2*m1*m2*n2 - m2**2*n1 - m2**2*n2 - n1**3 + n1**2*n2 + n1*n2**2 + n1*r1_sqr - n1*r2_sqr - n2**3 - n2*r1_sqr + n2*r2_sqr + (y1 + y2)*(m1**2 - 2*m1*m2 + m2**2 + n1**2 - 2*n1*n2 + n2**2))/(m1**2 - 2*m1*m2 + m2**2 + n1**2 - 2*n1*n2 + n2**2), (-m1**2 + m2**2 - n1**2 + n2**2 + r1_sqr - r2_sqr + 2*x2*(m1 - m2) + 2*y2*(n1 - n2)), (m1**4 - 4*m1**3*m2 + 6*m1**2*m2**2 + 2*m1**2*n1**2 + 2*m1**2*n2**2 - 2*m1**2*r1_sqr - 2*m1**2*r2_sqr - 4*m1*m2**3 - 4*m1*m2*n1**2 - 4*m1*m2*n2**2 + 4*m1*m2*r1_sqr + 4*m1*m2*r2_sqr + m2**4 + 2*m2**2*n1**2 + 2*m2**2*n2**2 - 2*m2**2*r1_sqr - 2*m2**2*r2_sqr + n1**4 - 2*n1**2*n2**2 - 2*n1**2*r1_sqr + 2*n1**2*r2_sqr + n2**4 + 2*n2**2*r1_sqr - 2*n2**2*r2_sqr + r1_sqr**2 - 2*r1_sqr*r2_sqr + r2_sqr**2 + 4*y2**2*(m1**2 - 2*m1*m2 + m2**2 + n1**2 - 2*n1*n2 + n2**2) - 4*y2*(m1**2*n1 + m1**2*n2 - 2*m1*m2*n1 - 2*m1*m2*n2 + m2**2*n1 + m2**2*n2 + n1**3 - n1**2*n2 - n1*n2**2 - n1*r1_sqr + n1*r2_sqr + n2**3 + n2*r1_sqr - n2*r2_sqr))/(4*(m1**2 - 2*m1*m2 + m2**2 + n1**2 - 2*n1*n2 + n2**2))])
        # Variable*distance = 1:
        distance_equation = Eq(((x1-x2)**2 + (y1-y2)**2)* d, 1)
        self.optimized_eqs.append((d*(m1**4 - 4*m1**3*m2 + 6*m1**2*m2**2 + 2*m1**2*n1**2 - 4*m1**2*n1*n2 + 2*m1**2*n2**2 - 2*m1**2*r1_sqr - 2*m1**2*r2_sqr - 4*m1*m2**3 - 4*m1*m2*n1**2 + 8*m1*m2*n1*n2 - 4*m1*m2*n2**2 + 4*m1*m2*r1_sqr + 4*m1*m2*r2_sqr + m2**4 + 2*m2**2*n1**2 - 4*m2**2*n1*n2 + 2*m2**2*n2**2 - 2*m2**2*r1_sqr - 2*m2**2*r2_sqr + n1**4 - 4*n1**3*n2 + 6*n1**2*n2**2 - 2*n1**2*r1_sqr - 2*n1**2*r2_sqr - 4*n1*n2**3 + 4*n1*n2*r1_sqr + 4*n1*n2*r2_sqr + n2**4 - 2*n2**2*r1_sqr - 2*n2**2*r2_sqr + r1_sqr**2 - 2*r1_sqr*r2_sqr + r2_sqr**2) + m1**2 - 2*m1*m2 + m2**2 + n1**2 - 2*n1*n2 + n2**2))
        # Exact distance:
        # D_squared = (circle1.center.x - circle2.center.x)**2 + (circle1.center.y - circle2.center.y)**2
        # distance_equation = Eq(((x1-x2)**2 + (y1-y2)**2), 4*circle1.squared_radius + ((circle1.squared_radius - circle2.squared_radius + D_squared)**2)/D_squared)
        return [[circle1.get_equation([x1, y1]), circle2.get_equation([x1, y1]), circle1.get_equation([x2, y2]), circle2.get_equation([x2, y2]), distance_equation], p1, p2]

    def intersect_line_circle(self, line, circle, point_coordinator=None):
        # If point_coordinator: [equations, further_point, closer_point] in order to sum segments easily
        p1 = self.create_point()
        x1 = p1.x
        y1 = p1.y
        p2 = self.create_point()
        x2 = p2.x
        y2 = p2.y
        a, b, c = line.a(), line.b(), line.c()
        r_squared = circle.squared_radius
        m, n = circle.center.x, circle.center.y
        self.optimized_eqs.extend([(2*a**2*b*n + a**2*c - 2*a*b**2*m + a*x1*(a**2 + b**2) - b**2*c - b*y2*(a**2 + b**2))/(a**2 + b**2), (-2*a**2*n + 2*a*b*m + 2*b*c + (a**2 + b**2)*(y1 + y2))/(a**2 + b**2), (a*x2 + b*y2 + c), (a**2*m**2 + a**2*n**2 - a**2*r_squared + 2*a*c*m + c**2 + y2**2*(a**2 + b**2) + 2*y2*(-a**2*n + a*b*m + b*c))/(a**2 + b**2)])
        # Variable*distance = 1:
        d = self.get_new_d(p1, p2)
        distance_equation = Eq(((x1-x2)**2 + (y1-y2)**2)* d, 1)
        self.optimized_eqs.append(d*(-4*a**2*m**2 + 4*a**2*r_squared - 8*a*b*m*n - 8*a*c*m - 4*b**2*n**2 + 4*b**2*r_squared - 8*b*c*n - 4*c**2) - a**2 - b**2)
        # Exact distance:
        # d_squared  = (((line.point2.y - line.point1.y)*circle.center.x - (line.point2.x-line.point1.x)*circle.center.y + line.point2.x*line.point1.y - line.point1.x*line.point2.y)**2)/((line.point1.x - line.point2.x)**2+(line.point1.y-line.point2.y)**2)
        # distance_equation = Eq(((x1-x2)**2 + (y1-y2)**2), 4*(circle.squared_radius - d_squared))
    
        if point_coordinator != None:
            c1 = point_coordinator.x
            d1 = point_coordinator.y
            coordinator_equation = Eq((x2-c1)**2 + (y2-d1)**2 - ((x1-c1)**2+(y1-d1)**2), self.get_new_d()**2)
            return [[line.get_equation([x1, y1]), circle.get_equation([x1, y1]), line.get_equation([x2, y2]), circle.get_equation([x2, y2]), distance_equation, coordinator_equation], p1, p2]
        return [[line.get_equation([x1, y1]), circle.get_equation([x1, y1]), line.get_equation([x2, y2]), circle.get_equation([x2, y2]), distance_equation], p1, p2]

    def coincide_points(self, point1, point2):
        # Checks if points eventually coincide
        if point1.x == point2.x and point1.y == point2.y:
            return True
        else:
            return False

    def not_on_same_line(self, p1, p2, p3):
        d1 = self.get_d(p1, p2)
        d2 = self.get_d(p1, p3)
        d3 = self.get_d(p2, p3)
        self.add_equation(Eq((d2*d3-d1*d2-d1*d3)*self.get_new_d(), 1))

    def get_d(self, point1, point2):
        for d in self.distances:
            if (d[1] == point1 and d[2] == point2) or (d[1] == point2 and d[2] == point1):
                return d[0]

    def prevent_duplicate_points(self, lst, object1, object2):
        # Prevents duplicate points
        equations = lst[0]
        duplicates = []
        p1 = lst[1]
        if len(lst) == 3:
            p2 = lst[2]
            duplicate_point = p2
            for point in self.points:
                if point == p1 or point == p2:
                    continue
                elif point.lie_on(object1) and point.lie_on(object2):
                    equations = [eq.subs({duplicate_point.x: point.x, duplicate_point.y: point.y}) for eq in equations]
                    self.all_vars.remove(duplicate_point.x)
                    self.all_vars.remove(duplicate_point.y)
                    self.new_variable_counter -= 2
                    self.points.remove(duplicate_point)
                    if duplicate_point == p2:
                        p2 = point
                        duplicates.append((duplicate_point, point))
                    else:
                        p1 = point
                        duplicates.append((duplicate_point, point))
                        break
                    duplicate_point = p1

        else:
            for point in self.points:
                if point == p1:
                    continue
                elif point.lie_on(object1) and point.lie_on(object2):
                    equations = [eq.subs({p1.x: point.x, p1.y: point.y})
                                 for eq in equations]
                    self.all_vars.remove(p1.x)
                    self.all_vars.remove(p1.y)
                    self.new_variable_counter -= 2
                    self.points.remove(p1)
                    p1 = point
                    duplicates.append((duplicate_point, point))
                    break
        return [equations, p1, p2, duplicates] if len(lst) == 3 else [equations, p1, duplicates]

    def get_new_var(self):
        index = 1
        while True:
            self.new_variable_counter += 1
            if self.new_variable_counter % 2 != 0:
                symb = Symbol(f'x{index}')
            else:
                symb = Symbol(f'y{index}')
                index += 1
            if symb not in self.all_vars:
                self.all_vars.append(symb)
                return symb

    def get_new_d(self, point1=None, point2=None):
        index = 1
        while True:
            symb = Symbol(f'd{index}')
            index += 1
            if symb not in self.all_vars:
                self.all_vars.append(symb)
                self.distances.append([symb, point1, point2])
                return symb

    def add_equation(self, equation):
        if equation != True:
            self.system.append(equation)


class Point:
    def __init__(self, x, y, construction=None):
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
            return None

    def to_str(self):
        return f"Point({self.x},{self.y}) : {type(self).__name__}"


class AribitaryPoint(Point):
    def __init__(self, construction, geometrical_object=None, distance: Optional[float] = None, coordinates: Optional[list] = None):
        if distance is None:
            distance = 0
        self.construction = construction
        if coordinates == None:
            self.x = construction.get_new_var()
            self.y = construction.get_new_var()
        else:
            self.x = coordinates[0]
            self.y = coordinates[1]
        self.construction.points.append(self)

        if geometrical_object is not None:
            if distance == 0:
                construction.add_equation(
                    Eq(geometrical_object.get_equation([self.x, self.y]).lhs, 0))
            else:
                if isinstance(geometrical_object, Line):
                    construction.add_equation(
                        Eq(geometrical_object.get_equation([self.x, self.y]).lhs ** 2,
                           (geometrical_object.a() ** 2 + geometrical_object.b() ** 2) * distance ** 2)
                    )
                elif isinstance(geometrical_object, Circle):
                    construction.add_equation(
                        Eq(geometrical_object.get_equation([self.x, self.y]).lhs ** 2,
                           geometrical_object.get_squared_radius() + 2 * geometrical_object.get_squared_radius() ** 0.5 * distance + distance ** 2)
                    )
                else:
                    raise TypeError("Unsupported geometrical object type")


class Line:
    def __init__(self, point1, point2, construction=None):
        self.point1 = point1
        self.point2 = point2
        if construction.coincide_points(point1, point2):
            raise ValueError(f"The line is not determined as the two given points ({
                             point1.x},{point1.y}) and ({point2.x},{point2.y}) coincide.")

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
    def __init__(self, center, point_on_circle, construction=None):
        self.center = center
        self.point_on_circle = point_on_circle
        if construction != None and construction.coincide_points(center, point_on_circle):
            raise ValueError(
                f"The circle coincides with its center ({center.x},{center.y})")
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


def length_of_segment(p1, p2):
    return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**(1/2)


class Polygon:
    def __init__(self, *points, construction=None):
        self.points = points


class Triangle(Polygon):
    def __init__(self, *points, construction=None):
        if len(points) != 3:
            raise ValueError("A triangle must be defined by exactly 3 points.")
        self.points = points
        self.surface = abs((points[0].x*(points[1].y-points[2].y) + points[1].x*(
            points[2].y-points[0].y) + points[2].x*(points[0].y-points[1].y))/2)


class Square(Polygon):
    def __init__(self, *points, construction=None):
        if len(points) != 4:
            raise ValueError("A square must be defined by exactly 4 points.")
        self.points = points
        self.squared_side = Circle(points[0], points[1]).squared_radius
        self.surface = self.squared_side