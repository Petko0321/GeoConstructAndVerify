from sympy import solve, symbols, simplify, fraction, collect, nsimplify
from basics import AribitaryPoint, Point, Construction, Square, coincide_points


def perpendicular_bisector(point1, point2, only_line=True, optimized=True):
    """Constructs the perpendicular bisector of the line segment between two points.

    This method finds the perpendicular bisector of the segment defined by `point1`
    and `point2`. The bisector will pass through the midpoint of the segment and
    be perpendicular to the line connecting the two points.

    Parameters:
    - point1: The first endpoint of the line segment.
    - point2: The second endpoint of the line segment.
    - only_line (bool, optional): If True, returns only the perpendicular bisector as a Line object.

    Returns:
    - Equations derived from the construction.
    - The intersecting points that determine the perpendicular bisector.
    - The perpendicular bisector as a Line object.
    """
    if point1.construction == None or point1.construction != point2.construction:
        raise ValueError("The objects have to be in the same construction!")
    construction: Construction = point1.construction
    if optimized:
        a1, b1, a2, b2 = point1.x, point1.y, point2.x, point2.y
        perpendicular_bisector = construction.define_line_by_equation(
            a1-a2, b1-b2, (a2**2-a1**2+b2**2-b1**2)/2)
        equations = []
        p1, p2 = None, None
    else:
        c1 = construction.create_circle(point1, point2)
        c2 = construction.create_circle(point2, point1)
        equations, p1, p2 = construction.intersect(c1, c2, False)
        perpendicular_bisector = construction.create_line(p1, p2)
    # construction.optimization_equations.extend(p1.x)
    if only_line:
        return perpendicular_bisector
    else:
        return [equations, p1, p2, perpendicular_bisector]

    # If we wanted to return the equation of the perpendicular bisector, we'd used this:
    # intersecting_points = solve(equations,construction.vars)
    # l2 = Line(Point(intersecting_points[0][0], intersecting_points[0][1]), Point(intersecting_points[1][0], intersecting_points[1][1]))
    # return simplify(l2.get_equation([x, y]))
    # But it's too slow


def midpoint(point1, point2, opimized=True):
    """Finds the midpoint of two given points.

    Parameters:
    - point1: The first point (tuple or list of coordinates).
    - point2: The second point (tuple or list of coordinates).

    Returns:
    - The midpoint as a Point object.
    """
    if point1.construction == None or point1.construction != point2.construction:
        raise ValueError("The objects have to be in the same construction!")
    construction: Construction = point1.construction
    if opimized:
        return construction.get_point((point1.x+point2.x)/2, (point1.y+point2.y)/2)
    line1 = construction.create_line(point1, point2)
    perpendicular_bisector1 = perpendicular_bisector(point1, point2)
    p = construction.intersect(line1, perpendicular_bisector1)
    return p


def angle_bisector(point1, point2, point3, only_line=True):
    """Constructs the angle bisector of an angle formed by three points.

    This method finds the bisector of the angle formed at `point2` by the lines
    passing through (`point1`, `point2`) and (`point2`, `point3`).

    Parameters:
    - point1: The first point defining one side of the angle.
    - point2: The vertex of the angle.
    - point3: The third point defining the other side of the angle.
    - only_line (bool, optional): If True, returns only the angle bisector as a Line object.

    Returns:
    - Equations derived from the construction.
    - The angle bisector as a Line object.
    """
    if point1.construction == None or point1.construction != point2.construction or point1.construction != point3.construction:
        raise ValueError("The objects have to be in the same construction!")
    construction: Construction = point1.construction
    all_equations = []
    line1 = construction.create_line(point2, point3)
    cr1 = construction.create_circle(point2, point1)
    equations, _, p = construction.intersect(cr1, line1, False, point3)
    # closer point to point3 ensures the angle bisecor is internal
    all_equations.extend(equations)
    equations, _, _, angle_bisector = perpendicular_bisector(point1, p, False)
    all_equations.extend(equations)
    if only_line:
        return angle_bisector
    else:
        return [equations, angle_bisector]


def perpendicular_line(point, line, point_is_on_line: bool = None, only_line: bool = True):
    """Constructs a line perpendicular to a given line through a specified point.

    This method determines a perpendicular line based on whether the given point
    lies on the provided line. Two different construction routes are used
    depending on this condition.

    Parameters:
    - point: The point through which the perpendicular line will pass.
    - line: The original line to which the new line will be perpendicular.
    - point_is_on_line (bool, optional): Specifies whether the given point is on the line.
      If None, this will be determined automatically.
    - only_line (bool, optional): If True, returns only the perpendicular line as a Line object.

    Returns:
    - Equations derived from the construction.
    - The intersecting points that determine the perpendicular line.
    - The perpendicular line as a Line object.
    """

    all_equations = []
    if point_is_on_line == None:
        point_is_on_line = point.lie_on(line)
    if point.construction == None or point.construction != line.point1.construction:
        raise ValueError("The objects have to be in the same construction!")
    construction: Construction = point.construction

    if point_is_on_line:
        another_point_on_line = line.point1
        if coincide_points(point, line.point1):
            another_point_on_line = line.point2
        c1 = construction.create_circle(point, another_point_on_line)
        equations, p1, p2 = construction.intersect(c1, line, False)
        all_equations.extend(equations)
        equations, p1, p2, perpendicular_line = perpendicular_bisector(
            p1, p2, False)
        all_equations.extend(equations)

    else:
        c1 = construction.create_circle(line.point1, point)
        c2 = construction.create_circle(line.point2, point)
        equations, p1, p2 = construction.intersect(c1, c2, False)
        for eq in equations:
            all_equations.append(eq)
        perpendicular_line = construction.create_line(p1, p2)
    if only_line:
        return perpendicular_line
    else:
        return [all_equations, p1, p2, perpendicular_line]


def parallel_line(point, line, only_line=True):
    """This method creates a parallel line passing through a point that does not lie on the given line.

    Parameters:
    - point: The point through which the parallel line will pass.
    - line: The original line to which the new line will be parallel.
    - only_line (bool, optional): If True, returns only the parallel line as a Line object.

    Returns:
    - Equations derived from the construction.
    - The intersecting points that determine the parallel line.
    - The parallel line as a Line object.
    """
    all_equations = []
    equations, _, _, perpendicular_line1 = perpendicular_line(
        point, line, False, False)
    all_equations.extend(equations)
    # point_in_on_line is given false
    equations, p1, p2, parallel_line = perpendicular_line(
        point, perpendicular_line1, True, False)
    all_equations.extend(equations)
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


def translate_vector(vector, point, only_vector=True, optimized=True):
    """Translates a vector using a given point.

    This method constructs a parallelogram to determine the translated vector.
    Note: It does not work if all points are collinear.

    Parameters:
    - vector: The vector to be translated.
    - point: A reference point for the translation.
    - only_vector (bool, optional): If True, returns only the translated vector.

    Returns:
    - Equations derived from the construction.
    - The fourth vertex of the parallelogram.
    - (or only) the translated vector.
    """

    if point.construction == None or point.construction != vector.starting_point.construction:
        raise ValueError("The objects have to be in the same construction!")
    construction: Construction = point.construction
    p1 = vector.starting_point
    p2 = vector.ending_point
    p3 = point
    all_equations = []
    if optimized:
        p = construction.get_point(p3.x+p2.x-p1.x, p3.y+p2.y-p1.y, )
        wanted_vector = Vector(p3, p)
    else:
        line1 = construction.create_line(p1, p2)
        line2 = construction.create_line(p1, p3)
        equations, _, _, line3 = parallel_line(p3, line1, False)
        all_equations.extend(equations)
        equations, _, _, line4 = parallel_line(p2, line2, False)
        all_equations.extend(equations)
        equations, p = construction.intersect(line3, line4, False)
        all_equations.extend(equations)
        wanted_vector = Vector(p3, p)
    if only_vector:
        return wanted_vector
    else:
        return [all_equations, p, wanted_vector]


def translate(vector, point, only_vector=True, optimized=True):
    """Translate a vector method (enhanced).

    Parameters:
    - vector: The vector to be translated.
    - point: A reference point for the translation.

    Returns:
    - Equations derived from the construction
    - The fourth vertex of the parallelogram
    - (or only) the translated vector
    """
    if point.construction == None or point.construction != vector.starting_point.construction:
        raise ValueError("The objects have to be in the same construction!")
    construction: Construction = point.construction
    p1 = vector.starting_point
    p2 = vector.ending_point
    p3 = point
    all_equations = []
    if optimized:
        p = construction.get_point(p3.x+p2.x-p1.x, p3.y+p2.y-p1.y)
        wanted_vector = Vector(p3, p)
    else:
        line1 = construction.create_line(p1, p2)
        if p3.lie_on(line1):
            print("The point lies on the line")
            equations, _, v1 = translate_vector(
                vector, construction.get_arbitrary_point(line1, 1), False, False)
            all_equations.extend(equations)
            equations, p, wanted_vector = translate_vector(
                v1, point, False, False)
            all_equations.extend(equations)
        else:
            print("The point does not lie on the line")
            all_equations, p, wanted_vector = translate_vector(vector, point, False, False)
    # print(f"The wanted vectror is from ({wanted_vector.starting_point.x}, {wanted_vector.starting_point.y}) to ({wanted_vector.ending_point.x}, {wanted_vector.ending_point.y})")
    if only_vector:
        return wanted_vector
    return all_equations, p, wanted_vector


def compass(point1, point2, point3, only_circle=True):
    """This function constructs a circle that is centered at `point3` with a radius equal to the distance
    between `point1` and `point2`.

    Parameters:
    - point1: A reference point used to determine the radius.
    - point2: A reference point used to determine the radius.
    - point3: The center of the constructed circle.
    - only_circle (bool, optional): If True, returns only the Circle object.

    Returns:
    - Equations derived from the construction.
    - The circle as a Circle object.
    """
    if point1.construction == None or point1.construction != point2.construction or point1.construction != point3.construction:
        raise ValueError("The objects have to be in the same construction!")
    construction: Construction = point1.construction
    equations, p, _ = translate(Vector(point1, point2), point3, False)
    circle = construction.create_circle(point3, p)
    if only_circle:
        return circle
    return [equations, circle]


def circle_through_3_points(point1, point2, point3, only_circle=True):
    """Constructs a circle passing through three given points.

    This method determines the unique circle that passes through the points
    `point1`, `point2`, and `point3`. The center of the circle and its radius
    are derived based on these points.

    Parameters:
    - point1: The first point on the circle.
    - point2: The second point on the circle.
    - point3: The third point on the circle.
    - only_circle (bool, optional): If True, returns only the Circle object.

    Returns:
    - Equations derived from the construction.
    - The center of the circle.
    - The circle as a Circle object.
    """
    if point1.construction == None or point1.construction != point2.construction or point1.construction != point3.construction:
        raise ValueError("The objects have to be in the same construction!")
    construction: Construction = point1.construction
    all_equations = []
    equations, _, _, perpendicular_bisector1 = perpendicular_bisector(point1, point2, False)
    all_equations.extend(equations)
    equations, _, _, perpendicular_bisector2 = perpendicular_bisector(point2, point3, False)
    all_equations.extend(equations)
    equations, center = construction.intersect(perpendicular_bisector1, perpendicular_bisector2, False)
    all_equations.extend(equations)
    circle = construction.create_circle(center, point1)
    # construction.add_equation(circle.get_equation([point2.x, point2.y]))
    # construction.add_equation(circle.get_equation([point3.x, point3.y]))
    if only_circle:
        return circle
    else:
        return [all_equations, center, circle]


def circle_by_diameter(point1, point2):
    """Constructs a circle given two points as the diameter endpoints.

    This method determines the circle whose diameter is defined by the points
    `point1` and `point2`. The center of the circle is the midpoint of the two
    points, and the radius is half the distance between them.

    Parameters:
    - point1: The first endpoint of the diameter.
    - point2: The second endpoint of the diameter.

    Returns:
    - The circle defined by the two points as the diameter.
    """
    if point1.construction == None or point1.construction != point2.construction:
        raise ValueError("The objects have to be in the same construction!")
    construction: Construction = point1.construction
    center = midpoint(point1, point2)
    circle = construction.create_circle(center, point1)
    return circle


def construct_square(point1, point2):
    """Constructs a square with a side length equal to the distance between two given points.

    This method creates a square where the side length is determined by the distance
    between `point1` and `point2`. The square is oriented with one side aligned with
    the line segment defined by the two points.

    Parameters:
    - point1: The first point defining one end of the square's side.
    - point2: The second point defining the other end of the square's side.

    Returns:
    - The square as a Square object.
    """
    if point1.construction == None or point1.construction != point2.construction:
        raise ValueError("The objects have to be in the same construction!")
    construction: Construction = point1.construction
    line1 = construction.create_line(point1, point2)
    cr1 = construction.create_circle(point2, point1)
    perpendicular_line1 = perpendicular_line(point2, line1, True)
    point3, _ = construction.intersect(cr1, perpendicular_line1)
    cr2 = construction.create_circle(point1, point2)
    cr3 = construction.create_circle(point3, point2)
    point4, _ = construction.intersect(cr2, cr3)
    square = Square(point1, point2, point3, point4)
    return Square

def simplify_expressions(expressions):
    num_polynomials = []
    denom_polynomials = []
    for expr in expressions:
        expr = simplify(expr)
        num, denom = fraction(expr)
        num_polynomials.append(num)
        denom_polynomials.append(denom)
    return num_polynomials, denom_polynomials

def reduce_quadratics(polynomials, variables):
    modified_polynomials = []
    variables = set(variables)
    
    for poly in polynomials:
        updated = False
        vars = poly.free_symbols
        coeffs = poly.as_coefficients_dict()
        for var in (variables & vars):
            
            a = poly.coeff(var, 2)
            b = poly.coeff(var, 1)
            c = poly.coeff(var, 0)
            
            if a != 0:
                discriminant = simplify(b**2 - 4*a*c)
                print(discriminant)
                if discriminant == 0 or discriminant.equals(0) or nsimplify(discriminant) == 0:
                    root = -b / (2*a)
                    linear_eq = var - root
                    modified_polynomials.append(linear_eq)
                    updated = True
                    break  
        
        if not updated:
            modified_polynomials.append(poly)
    
    return modified_polynomials