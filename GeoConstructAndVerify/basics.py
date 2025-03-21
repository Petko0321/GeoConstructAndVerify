from sympy import Symbol, simplify, Expr, solve, symbols, Symbol, simplify, ring, RR, groebner, expand
from collections import defaultdict


class Construction:
    def __init__(self, *geometric_objects, input_equations=None):
        self.system = []
        self.distances = []
        self.all_vars = []
        self.points = []
        self.input_vars = []
        self.solution = Solution(self)
        self.objects = set()
        for obj in geometric_objects:
            if isinstance(obj, Point):
                self.update_points(obj, are_input=True)
            elif isinstance(obj, Line):
                self.update_points(obj.point1, obj.point2, are_input=True)
                self.objects.add(obj)
            elif isinstance(obj, Circle):
                self.update_points(
                    obj.center, obj.point_on_circle, are_input=True)
                self.objects.add(obj)
            elif isinstance(obj, Polygon):
                self.update_points(*obj.points, are_input=True)
            else:
                raise ValueError("Unsupported geometrical object type")
        for point in self.points:
            self.input_vars.extend([point.x, point.y])

        self.last_d_index = 0
        # Ensure the input points are distinct
        for i in range(len(self.points)):
            for j in range(i + 1, len(self.points)):
                point1 = self.points[i]
                point2 = self.points[j]
                self.not_coinciding(point1, point2)
        self.input_eqs = [eq for eq in self.system]
        self.all_vars.extend(self.input_vars)
        self.points = self.points
        if input_equations != None:
            for eq in input_equations:
                self.add_equation(eq)
        self.new_variable_counter = 0
        self.optimization_equations = []
        self.arbitrary_points = []
        self.output_object = []

    def update_points(self, *points, are_input=False):
        for point in points:
            if not are_input:
                if not isinstance(point, AribitaryPoint):
                    self.solution.auxiliary_vars.extend([point.x, point.y])
                else:
                    self.solution.synthetic_vars.extend([point.x, point.y])
            else:
                point.construction = self
        if are_input:
            self.points.extend(points)

    def update_solution(self, equations):
        self.solution.system.extend(equations)

    def create_point(self):
        new_point = Point(self.get_new_var(), self.get_new_var(), self)
        self.points.append(new_point)
        return new_point

    def get_arbitrary_point(self, object=None, distance: float = None):
        return AribitaryPoint(self, object, distance)

    def get_collinear_point(self, object):
        return AribitaryPoint(self, object)

    def get_point(self, x, y):
        point = Point(x, y, self)
        self.points.append(point)
        return point

    def create_line(self, point1, point2):
        new_line = Line(point1, point2, self)
        self.objects.add(new_line)
        return new_line

    def create_circle(self, center, point_on_circle):
        new_circle = Circle(center, point_on_circle, self)
        self.objects.add(new_circle)
        return new_circle

    def define_line_by_equation(self, a, b, c):
        line = Line(None, None, self)
        line.set_equation(a, b, c)
        return line

    def intersect(self, line_or_circle1, line_or_circle2, only_points: bool = True, point_coordinator=None):
        # self.optimized_eqs = []
        if isinstance(line_or_circle1, Line) and isinstance(line_or_circle2, Line):
            intersecting_point = self.evaluate_presence_of_intersecting_point(
                line_or_circle1, line_or_circle2)
            if intersecting_point:
                if only_points:
                    return intersecting_point
                else:
                    return [[], intersecting_point]
            else:
                equations, point = self.intersect_two_lines(
                    line_or_circle1, line_or_circle2)
        elif isinstance(line_or_circle1, Circle) and isinstance(line_or_circle2, Circle):
            first_point, second_point = self.evevaluate_presence_two_circles(
                line_or_circle1, line_or_circle2)
            if first_point:
                if only_points:
                    return [first_point, second_point]
                else:
                    return [[], first_point, second_point]
            elif second_point:
                equations, first_point, second_point = self.intersect_two_circles(
                    line_or_circle1, line_or_circle2, second_point)
            else:
                equations, first_point, second_point = self.intersect_two_circles(
                    line_or_circle1, line_or_circle2)
        elif isinstance(line_or_circle1, Line) and isinstance(line_or_circle2, Circle):
            first_point, second_point = self.evaluate_presence_line_circle(
                line_or_circle1, line_or_circle2)
            if first_point:
                if only_points:
                    return [first_point, second_point]
                else:
                    return [[], first_point, second_point]
            elif second_point:
                equations, first_point, second_point = self.intersect_line_circle(
                    line_or_circle1, line_or_circle2, second_point, point_coordinator)
            else:
                equations, first_point, second_point = self.intersect_line_circle(
                    line_or_circle1, line_or_circle2, point_coordinator=point_coordinator)
        elif isinstance(line_or_circle1, Circle) and isinstance(line_or_circle2, Line):
            first_point, second_point = self.evaluate_presence_line_circle(
                line_or_circle2, line_or_circle1)
            if first_point:
                if only_points:
                    return [first_point, second_point]
                else:
                    return [[], first_point, second_point]
            elif second_point:
                equations, first_point, second_point = self.intersect_line_circle(
                    line_or_circle2, line_or_circle1, second_point, point_coordinator)
            else:
                equations, first_point, second_point = self.intersect_line_circle(
                    line_or_circle2, line_or_circle1, point_coordinator=point_coordinator)
        else:
            print(line_or_circle1)
            print(line_or_circle2)
            raise ValueError("Invalid geometrical object type!")
        equations = [eq for eq in equations if eq not in set(self.system)]
        self.update_solution(equations)
        self.system.extend(equations)

        # for visualization purposes
        for eq in equations:
            print(eq)
        if isinstance(line_or_circle1, Line) and isinstance(line_or_circle2, Line):
            print(
                f"--> coordinates ({point.x},{point.y}) of the intersecting point")
        else:
            print(
                f"--> coordinates ({first_point.x},{first_point.y}), ({second_point.x},{second_point.y}) of the two intersecting points")
        # return result
        if isinstance(line_or_circle1, Line) and isinstance(line_or_circle2, Line):
            if only_points:
                return point
            return [equations, point]
        else:
            if only_points:
                return [first_point, second_point]
            return [equations, first_point, second_point]

    def intersect_two_lines(self, line1, line2):
        p = self.create_point()
        self.update_points(p)
        x = p.x
        y = p.y
        # a1, b1, c1 = line1.a(), line1.b(), line1.c()
        # a2, b2, c2 = line2.a(), line2.b(), line2.c()
        # self.optimized_eqs.extend(
        #     [x*(a1*b2 - a2*b1) - (b1*c2 - b2*c1), y*(a1*b2 - a2*b1) - (a2*c1 - a1*c2)])
        return [[line1.get_equation([x, y]), line2.get_equation([x, y])], p]

    def intersect_two_circles(self, circle1, circle2, intersecting_point=False):
        equations = []
        if intersecting_point:
            p1 = self.create_point()
            p2 = intersecting_point
            self.update_points(p1)
            d = self.get_new_d(p1, p2)
            distance_equation = simplify(
                ((p1.x-p2.x)**2 + (p1.y-p2.y)**2) * d - 1)
            equations.extend([circle1.get_equation(
                [p1.x, p1.y]), circle2.get_equation([p1.x, p1.y]), distance_equation])
        else:
            p1 = self.create_point()
            p2 = self.create_point()
            self.update_points(p1, p2)
            d = self.get_new_d(p1, p2)
            distance_equation = simplify(
                ((p1.x-p2.x)**2 + (p1.y-p2.y)**2) * d - 1)
            eq1 = circle1.get_equation([p1.x, p1.y])
            eq2 = circle2.get_equation([p1.x, p1.y])
            eq3 = circle1.get_equation([p2.x, p2.y])
            eq4 = circle2.get_equation([p2.x, p2.y])
            equations.extend([eq1, simplify(expand(eq1)-expand(eq2)),
                             eq3, simplify(expand(eq3)-expand(eq4)), distance_equation])
        # m1, n1 = circle1.center.x, circle1.center.y
        # m2, n2 = circle2.center.x, circle2.center.y
        # r1_sqr = circle1.squared_radius
        # r2_sqr = circle2.squared_radius
        # self.optimized_eqs.extend([(x1*(m1 - m2)*(m1**3 - 3*m1**2*m2 + 3*m1*m2**2 + m1*n1**2 - 2*m1*n1*n2 + m1*n2**2 - m2**3 - m2*n1**2 + 2*m2*n1*n2 - m2*n2**2) - y2*(n1 - n2)*(m1**3 - 3*m1**2*m2 + 3*m1*m2**2 + m1*n1**2 - 2*m1*n1*n2 + m1*n2**2 - m2**3 - m2*n1**2 + 2*m2*n1*n2 - m2*n2**2) + (m1 - m2)*(-m1**4 + 2*m1**3*m2 + 2*m1**2*n1*n2 - 2*m1**2*n2**2 + m1**2*r1_sqr - m1**2*r2_sqr - 2*m1*m2**3 - 2*m1*m2*n1**2 + 2*m1*m2*n2**2 - 2*m1*m2*r1_sqr + 2*m1*m2*r2_sqr + m2**4 + 2*m2**2*n1**2 - 2*m2**2*n1*n2 + m2**2*r1_sqr - m2**2*r2_sqr + n1**4 - 2*n1**3*n2 - n1**2*r1_sqr + n1**2*r2_sqr + 2*n1*n2**3 + 2*n1*n2*r1_sqr - 2*n1*n2*r2_sqr - n2**4 - n2**2*r1_sqr + n2**2*r2_sqr)/2), (-m1**2*n1 - m1**2*n2 + 2*m1*m2*n1 + 2*m1*m2*n2 - m2**2*n1 - m2**2*n2 - n1**3 + n1**2*n2 + n1*n2**2 + n1*r1_sqr - n1*r2_sqr - n2**3 -
        #                           n2*r1_sqr + n2*r2_sqr + (y1 + y2)*(m1**2 - 2*m1*m2 + m2**2 + n1**2 - 2*n1*n2 + n2**2)), (-m1**2 + m2**2 - n1**2 + n2**2 + r1_sqr - r2_sqr + 2*x2*(m1 - m2) + 2*y2*(n1 - n2)), (m1**4 - 4*m1**3*m2 + 6*m1**2*m2**2 + 2*m1**2*n1**2 + 2*m1**2*n2**2 - 2*m1**2*r1_sqr - 2*m1**2*r2_sqr - 4*m1*m2**3 - 4*m1*m2*n1**2 - 4*m1*m2*n2**2 + 4*m1*m2*r1_sqr + 4*m1*m2*r2_sqr + m2**4 + 2*m2**2*n1**2 + 2*m2**2*n2**2 - 2*m2**2*r1_sqr - 2*m2**2*r2_sqr + n1**4 - 2*n1**2*n2**2 - 2*n1**2*r1_sqr + 2*n1**2*r2_sqr + n2**4 + 2*n2**2*r1_sqr - 2*n2**2*r2_sqr + r1_sqr**2 - 2*r1_sqr*r2_sqr + r2_sqr**2 + 4*y2**2*(m1**2 - 2*m1*m2 + m2**2 + n1**2 - 2*n1*n2 + n2**2) - 4*y2*(m1**2*n1 + m1**2*n2 - 2*m1*m2*n1 - 2*m1*m2*n2 + m2**2*n1 + m2**2*n2 + n1**3 - n1**2*n2 - n1*n2**2 - n1*r1_sqr + n1*r2_sqr + n2**3 + n2*r1_sqr - n2*r2_sqr))])
        # # Variable*distance = 1:
        # distance_equation = simplify(((x1-x2)**2 + (y1-y2)**2) * d - 1)
        # self.optimized_eqs.append((d*(m1**4 - 4*m1**3*m2 + 6*m1**2*m2**2 + 2*m1**2*n1**2 - 4*m1**2*n1*n2 + 2*m1**2*n2**2 - 2*m1**2*r1_sqr - 2*m1**2*r2_sqr - 4*m1*m2**3 - 4*m1*m2*n1**2 + 8*m1*m2*n1*n2 - 4*m1*m2*n2**2 + 4*m1*m2*r1_sqr + 4*m1*m2*r2_sqr + m2**4 + 2*m2**2*n1**2 - 4*m2**2*n1*n2 + 2*m2**2*n2 **
        #                           2 - 2*m2**2*r1_sqr - 2*m2**2*r2_sqr + n1**4 - 4*n1**3*n2 + 6*n1**2*n2**2 - 2*n1**2*r1_sqr - 2*n1**2*r2_sqr - 4*n1*n2**3 + 4*n1*n2*r1_sqr + 4*n1*n2*r2_sqr + n2**4 - 2*n2**2*r1_sqr - 2*n2**2*r2_sqr + r1_sqr**2 - 2*r1_sqr*r2_sqr + r2_sqr**2) + m1**2 - 2*m1*m2 + m2**2 + n1**2 - 2*n1*n2 + n2**2))
        # Exact distance:
        # D_squared = (circle1.center.x - circle2.center.x)**2 + (circle1.center.y - circle2.center.y)**2
        # distance_equation = simplify(((x1-x2)**2 + (y1-y2)**2) - 4*circle1.squared_radius - ((circle1.squared_radius - circle2.squared_radius + D_squared)**2)/D_squared)
        return [equations, p1, p2]

    def intersect_line_circle(self, line, circle, intersecting_point=False, point_coordinator=None):
        # If point_coordinator: [equations, further_point, closer_point] in order to sum segments easily
        equations = []
        if intersecting_point:
            p1 = self.create_point()
            p2 = intersecting_point
            self.update_points(p1)
            d = self.get_new_d(p1, p2)
            distance_equation = simplify(
                ((p1.x-p2.x)**2 + (p1.y-p2.y)**2) * d - 1)
            equations.extend([line.get_equation([p1.x, p1.y]), circle.get_equation(
                [p1.x, p1.y]), distance_equation])
        else:
            p1 = self.create_point()
            p2 = self.create_point()
            self.update_points(p1, p2)
            d = self.get_new_d(p1, p2)
            distance_equation = simplify(
                ((p1.x-p2.x)**2 + (p1.y-p2.y)**2) * d - 1)
            equations.extend([line.get_equation([p1.x, p1.y]), circle.get_equation(
                [p1.x, p1.y]), line.get_equation([p2.x, p2.y]), circle.get_equation([p2.x, p2.y]), distance_equation])
        # a, b, c = line.a(), line.b(), line.c()
        # r_squared = circle.squared_radius
        # m, n = circle.center.x, circle.center.y
        # self.optimized_eqs.extend([(2*a**2*b*n + a**2*c - 2*a*b**2*m + a*x1*(a**2 + b**2) - b**2*c - b*y2*(a**2 + b**2)), (-2*a**2*n + 2*a*b*m + 2*b*c + (
        #     a**2 + b**2)*(y1 + y2)), (a*x2 + b*y2 + c), (a**2*m**2 + a**2*n**2 - a**2*r_squared + 2*a*c*m + c**2 + y2**2*(a**2 + b**2) + 2*y2*(-a**2*n + a*b*m + b*c))])
        # # Variable*distance = 1:
        # d = self.get_new_d(p1, p2)
        # distance_equation = simplify(((x1-x2)**2 + (y1-y2)**2) * d - 1)
        # self.optimized_eqs.append(d*(-4*a**2*m**2 + 4*a**2*r_squared - 8*a*b*m*n -
        #                           8*a*c*m - 4*b**2*n**2 + 4*b**2*r_squared - 8*b*c*n - 4*c**2) - a**2 - b**2)
        # Exact distance:
        # d_squared  = (((line.point2.y - line.point1.y)*circle.center.x - (line.point2.x-line.point1.x)*circle.center.y + line.point2.x*line.point1.y - line.point1.x*line.point2.y)**2)/((line.point1.x - line.point2.x)**2+(line.point1.y-line.point2.y)**2)
        # distance_equation = simplify(((x1-x2)**2 + (y1-y2)**2)- 4*(circle.squared_radius - d_squared))
        if point_coordinator != None:
            c1 = point_coordinator.x
            d1 = point_coordinator.y
            coordinator_equation = simplify(
                (p1.x-c1)**2 + (p1.y-d1)**2 - ((p2.x-c1)**2+(p2.y-d1)**2) - self.get_new_d()**2)
            equations.append(coordinator_equation)
        return [equations, p1, p2]

    def not_collinear(self, p1, p2, p3):
        """
        This method ensures three points do not lie on a single line by 
        adding a equation that forces the determinant to be nonzero.
        As S_triangle = 1/2*|det| => points are collinear.
        """
        # d1 = self.get_d(p1, p2)
        # d2 = self.get_d(p1, p3)
        # d3 = self.get_d(p2, p3)
        # self.add_equation(simplify((d2*d3-d1*d2-d1*d3)*self.get_new_d()- 1))
        a1, b1 = p1.x, p1.y
        a2, b2 = p2.x, p2.y
        a3, b3 = p3.x, p3.y
        # Ensures that the three points are not congruent
        det = a1*b1 + a2*b3 + a3*b1 - a3*b2 - a1*b3 - a2*b1
        self.add_equation(det*self.get_new_d()-1)

    def not_coinciding(self, p1, p2):
        """
        This method ensures that two points (usually input or arbirary) do not coincide by
        adding a equation in the construction that enforces a nonzero distance between them.
        """
        d = self.get_new_d(p1, p2)
        self.add_equation(d*((p1.x-p2.x)**2+(p1.y-p2.y)**2)-1)

    def set_parallel(self, line1, line2):
        """
        This method ensures that two lines determined by two input or arbitrary points are parallel 
        by enforcing the necessary and sufficient condition to be satisfied.

        Given two lines g1: a1x + b1y + c1 = 0 and g2: a2x + b2y + c2 = 0
        g1||g2 <=> i) a1b2 = a2b1 and ii) c1 ≠ c2 (ensures they do not coincide)

        This enables the construction of trapezoids and many various constructions.
        """
        self.add_equation(line1.a()*line2.b() - line1.b()*line2.a())
        self.add_equation(self.get_new_d(line1.c()-line2.c())-1)

    def set_perpendicular(self, line1, line2):
        """
        This method ensures that two lines determined by two input or arbitrary points are perpendicular 
        by enforcing the necessary and sufficient condition to be satisfied.

         Given two lines g1: a1x + b1y + c1 = 0 and g2: a2x + b2y + c2 = 0
        g1_|_g2 <=> i) a1a2 + b1b2 = 0

        This enables the construction of rhombus and many various constructions.
        """
        self.add_equation(line1.a()*line2.a()+line1.b()*line2.b())

    def get_d(self, point1, point2):
        for d in self.distances:
            if (d[1] == point1 and d[2] == point2) or (d[1] == point2 and d[2] == point1):
                return d[0]

    def get_generators(self):
        return self.solution.synthetic_vars + self.solution.auxiliary_vars  + list(reversed(self.solution.distances))

    def evaluate_presence_of_intersecting_point(self, line1, line2):
        """
    This method checks if there exists a point among the present points that lies on both given lines.
    If such a point is found, it is returned as the intersection point.
    If no such point is found, the method returns False.
        """
        for point in self.points:
            if point.lie_on(line1) and point.lie_on(line2):
                return point
        return False

    def evaluate_presence_line_circle(self, line, circle):
        """
    Finds up to two points that lie on both the given line and circle.

    The first detected intersection is stored in `second_point`. If a second intersection is found,
    it is stored in `first_point`, and the search stops.

    Returns:
        [first_point, second_point] where:
        - `first_point` is the second detected intersection (or False if only one exists).
        - `second_point` is the first detected intersection (or False if none exist).
        """
        first_point = False
        second_point = False
        for point in self.points:
            if point.lie_on(line) and point.lie_on(circle):
                if second_point:
                    first_point = point
                    break
                else:
                    second_point = point
        return [first_point, second_point]

    def evevaluate_presence_two_circles(self, circle1, circle2):
        """
    Finds up to two points that lie on both the given line and circle.

    The first detected intersection is stored in `second_point`. If a second intersection is found,
    it is stored in `first_point`, and the search stops.

    Returns:
        [first_point, second_point] where:
        - `first_point` is the second detected intersection (or False if only one exists).
        - `second_point` is the first detected intersection (or False if none exist).
        """
        first_point = False
        second_point = False
        for point in self.points:
            if point.lie_on(circle1) and point.lie_on(circle2):
                if second_point:
                    first_point = point
                    break
                else:
                    second_point = point
        return [first_point, second_point]

    def prevent_duplicate(self, lst, object1, object2):
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
                    equations = [simplify(eq.subs(
                        {duplicate_point.x: point.x, duplicate_point.y: point.y})) for eq in equations]
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
        symb = Symbol(f'x{self.new_variable_counter//2+1}' if self.new_variable_counter %
                      2 == 0 else f'y{self.new_variable_counter//2+1}', real=True)
        self.new_variable_counter += 1
        return symb

    def get_new_d(self, point1=None, point2=None):
        symb = Symbol(f'd{self.last_d_index + 1}', real=True)
        self.last_d_index += 1
        self.all_vars.append(symb)
        self.solution.distances.append(symb)
        self.distances.append([symb, point1, point2])
        return symb

    def add_equation(self, equation):
        if equation != True:
            self.system.append(equation)

    def set_as_output(self, objec):
        self.output_object.append(objec)
        vars = []
        if isinstance(objec, Point):
            vars.extend(objec.coordinates)
        elif isinstance(objec, Line):
            vars.extend(objec.point1.coordinates)
            vars.extend(objec.point2.coordinates)
        elif isinstance(objec, Circle):
            vars.extend(objec.center.coordinates)
            vars.extend(objec.point_on_circle.coordinates)
        elif isinstance(objec, list):
            for i in objec:
                self.set_as_output(i)
        else:
            raise ValueError("Unsupported geometrical object type")
        self.solution.set_ouput_variables(vars)


class Solution:
    def __init__(self, construction: Construction, optimized=False):
        self.construction: Construction = construction
        self.input_vars = self.construction.input_vars
        self.output_vars = []
        self.auxiliary_vars = []
        self.synthetic_vars = []
        self.distances = []
        self.all_vars = []
        self.system = []
        self.values = {}
        # if optimized:
        #     system_eqs = construction.input_eqs + construction.optimization_equations
        # else:
        #     system_eqs = construction.system
        for eq in self.construction.system:
            if isinstance(eq, Expr):
                expr = eq
            else:
                raise ValueError("Unsupprorted equation type!")
            self.system.append(expr)
            # for var in construction.all_vars:
            #     if isinstance(var, Symbol):
            #         self.all_vars.append(var)
        # self.synthetic_vars = [
        #     var for arb_point in self.construction.arbitrary_points for var in arb_point.coordinates
        # ]
        # input_vars_set = set(self.input_vars)
        # output_vars_set = set(self.output_vars)
        # synthetic_vars_set = set(self.synthetic_vars)

        # seen = set()
        # self.auxiliary_vars = []
        # for var in self.all_vars:
        #     if var not in input_vars_set and var not in output_vars_set and var not in synthetic_vars_set:
        #         if var not in seen:
        #             self.auxiliary_vars.append(var)
        #             seen.add(var)
        # # ringg = ring(self.all_vars, RR)[0]
        # order = monomial_key(self.custom_order)
        # self.reduced_groebner_basis = groebner(self.system, self.all_vars, method="buchberger", order="grlex")

    def set_input_values(self, **values):
        """Set values for input and synthetic variables."""
        for var in (self.input_vars + self.synthetic_vars):
            if var.name in values:
                self.values[var] = values[var.name]

    def get_value(self, var):
        """Get the assigned value of a variable, if available."""
        return self.values.get(var, None)

    def get_system(self):
        return [eq.subs(self.values) for eq in self.construction.system]

    def set_ouput_variables(self, *output_vars):
        self.output_vars.extend(output_vars)

        # def custom_order(self, monomial):
    #     # Define the custom monomial order
    #     synthetic_part = monomial[:len(self.synthetic_vars)]
    #     output_part = monomial[len(self.synthetic_vars):len(
    #         self.synthetic_vars) + len(self.output_vars)]
    #     input_part = monomial[len(self.synthetic_vars) +
    #                           len(self.output_vars):]

    #     # Priority order: Synthetic > Output > Input
    #     return (tuple(-exp for exp in synthetic_part),
    #             tuple(-exp for exp in output_part),
    #             tuple(-exp for exp in input_part))


class Point:
    def __init__(self, x, y, construction=None):
        self.x = x
        self.y = y
        self.coordinates = (x, y)
        self.construction: Construction = construction

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, type(self)):
            return False
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def lie_on(self, obj):
        if simplify(obj.get_equation([self.x, self.y])) == 0:
            return True
        # elif object.get_equation([self.x, self.y]) in self.construction.system:
        #     return True
        else:
            return None

    def to_str(self):
        return f"Point({self.x},{self.y}) : {type(self).__name__}"
    # def str(self):
    #     return self.__hash__


class AribitaryPoint(Point):
    def __init__(self, construction, geometrical_object=None, distance: float = None, coordinates: list = None):
        if distance is None:
            distance = 0
        self.construction: Construction = construction
        if coordinates == None:
            self.x = construction.get_new_var()
            self.y = construction.get_new_var()
        else:
            self.x = coordinates[0]
            self.y = coordinates[1]
        self.coordinates = (self.x, self.y)
        self.construction.points.append(self)
        self.construction.arbitrary_points.append(self)
        self.construction.solution.synthetic_vars.extend([self.x, self.y])

        if geometrical_object is not None:
            if distance == 0:
                construction.add_equation(
                    simplify(geometrical_object.get_equation([self.x, self.y])))
            else:
                if isinstance(geometrical_object, Line):
                    construction.add_equation(
                        simplify(geometrical_object.get_equation([self.x, self.y])**2 -
                                 (geometrical_object.a() ** 2 + geometrical_object.b() ** 2) * distance ** 2)
                    )
                elif isinstance(geometrical_object, Circle):
                    construction.add_equation(
                        simplify(geometrical_object.get_equation([self.x, self.y]) ** 2 -
                                 geometrical_object.get_squared_radius() - 2 * geometrical_object.get_squared_radius() ** 0.5 * distance - distance ** 2)
                    )
                else:
                    raise TypeError("Unsupported geometrical object type")


def coincide_points(point1, point2):
    return point1.__eq__(point2)


def length_of_segment(p1, p2):
    return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**(1/2)


class Geometrical_obj:
    def __init__(self, construction):
        self.collinear_points = set()
        self.construction = construction

    def to_str(self):
        collinear_points_str = ", ".join(
            str(point.coordinates) for point in self.collinear_points)
        return f"Geometrical object: {type(self).__name__}; collinear points: {collinear_points_str}"

    def update_collinear_points(self, *points):
        if points == ():
            points = self.construction.points
        for point in points:
            if point.lie_on(self):
                self.collinear_points.add(point)


class Line(Geometrical_obj):
    def __init__(self, point1, point2, construction=None):
        super().__init__(construction)
        self.point1 = point1
        self.point2 = point2
        if point1 == None:
            self.a = 0
            self.b = 0
            self.c = 0
            self.equation = 0
        else:
            self.collinear_points.add(point1)
            self.collinear_points.add(point2)
            if coincide_points(point1, point2):
                raise ValueError(
                    f"The line is not determined as the two given points ({point1.x},{point1.y}) and ({point2.x},{point2.y}) coincide.")
            x1, y1 = self.point1.x, self.point1.y
            x2, y2 = self.point2.x, self.point2.y
            # Coefficients a, b, c for the line equation ax + by + c = 0
            self.a = y1 - y2
            self.b = x2 - x1
            self.c = x1 * y2 - x2 * y1
            self.equation = simplify(
                self.a * Symbol('x') + self.b * Symbol('y') + self.c)

    def get_equation(self, variables=None):
        if variables == None:
            return self.equation
        # Return the equation in the form ax + by + c = 0
        return self.equation.subs({Symbol('x'): variables[0], Symbol('y'): variables[1]})

    def set_equation(self, a, b, c):
        if self.point1 == None:
            self.a = a
            self.b = b
            self.c = c
            self.equation = simplify(
                self.a * Symbol('x') + self.b * Symbol('y') + self.c)
        else:
            print("Cannot set equation of line initially defined by two points!")


class Circle(Geometrical_obj):
    def __init__(self, center, point_on_circle, construction):
        if coincide_points(center, point_on_circle):
            raise ValueError(
                f"The circle coincides with its center ({center.x},{center.y})")
        super().__init__(construction)
        self.center = center
        self.point_on_circle = point_on_circle
        self.construction = construction
        self.collinear_points.add(point_on_circle)
        h, k = center.x, center.y
        x1, y1 = point_on_circle.x, point_on_circle.y
        self.squared_radius = (x1 - h)**2 + (y1 - k)**2
        self.equation = simplify(
            (Symbol('x') - h)**2 + (Symbol('y') - k)**2 - self.squared_radius)

    def get_equation(self, variables=None):
        if variables == None:
            return self.equation
        return self.equation.subs({Symbol('x'): variables[0], Symbol('y'): variables[1]})


class Polygon:
    def __init__(self, *points):
        self.points = points
        self.construction: Construction = points[0].construction


class Triangle(Polygon):
    def __init__(self, *points):
        if len(points) != 3:
            raise ValueError("A triangle must be defined by exactly 3 points.")
        self.construction: Construction = points[0].construction
        self.points = points
        self.surface = abs((points[0].x*(points[1].y-points[2].y) + points[1].x*(
            points[2].y-points[0].y) + points[2].x*(points[0].y-points[1].y))/2)


class Square(Polygon):
    def __init__(self, *points):
        if len(points) != 4:
            raise ValueError("A square must be defined by exactly 4 points.")
        self.construction: Construction = points[0].construction
        self.points = points
        self.squared_side = Circle(points[0], points[1]).squared_radius
        self.surface = self.squared_side
