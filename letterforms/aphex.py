import collections
import math
import random
import unittest

import svgwrite

Circle = collections.namedtuple('Circle', ['x', 'y', 'r'])
Segment = collections.namedtuple('Segment', ['x0', 'y0', 'x1', 'y1'])
Arc = collections.namedtuple('Arc', ['x0', 'y0', 'x1', 'y1', 'r', 'a', 'l', 's'])
LEFT = 'left'
RIGHT = 'right'

def mag_v(v):
    return math.sqrt(v[0]**2 + v[1]**2)

def distance_v(v1, v2):
    return mag_v(sub_v(v2, v1))

def norm_v(v):
    return (v[0] / mag_v(v), v[1] / mag_v(v))

def rotate_v(v, cw):
    if cw:
        return (-v[1], v[0])
    else:
        return (v[1], -v[0])

def scale_v(v, s):
    return (v[0] * s, v[1] * s)

def add_v(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])

def sub_v(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1])

def draw_v(dwg, p0, p1):
    dwg.add(dwg.line(p0, p1, stroke='green'))
    dwg.add(dwg.circle(p1, 3, stroke='green'))

def parallel_tangent_point(center_v1, center_v2, r, cw):
    """
    Method for handling circles of the same size based on this Stack Overflow:
    https://math.stackexchange.com/q/175906

    vector math notes:
    - a unit vector has a magnitude of 1; to convert a vector to it, you
      need to divide both components of the vector (the x and the y) by
      the vector's magnitude (the hypotenuse of the right triangle). So
      the magnitude is sqrt(x**2+y**2) by the Pythagorean theorem.
    - to rotate a vector 90 degrees:
        - CW: (x, y) -> (-y, x)
        - CCW: (x, y) -> (y, -x)
    """
    # vector from one circle center to the other
    v = sub_v(center_v2, center_v1)

    # unit vector for that vector
    unit = norm_v(v)

    # rotate 90 degrees
    rotated = rotate_v(unit, cw)

    # scale to length of circle radius
    scaled = scale_v(rotated, r)

    # add to "from" circle center
    return add_v(scaled, center_v1)

def parallel_tangent(c0, c1, side):
    """
    Called when the circles have the same radius and the tangent does
    not cross over (so only one side value is needed).
    """
    center0 = (c0.x, c0.y)
    center1 = (c1.x, c1.y)

    if side == LEFT:
        pt0 = parallel_tangent_point(center0, center1, c0.r, False)
        pt1 = parallel_tangent_point(center1, center0, c0.r, True)
    else:
        pt0 = parallel_tangent_point(center0, center1, c0.r, True)
        pt1 = parallel_tangent_point(center1, center0, c0.r, False)

    return Segment(pt0[0], pt0[1], pt1[0], pt1[1])

def tangent(c0, c1, side0, side1):
    """
    Calculates a tangent between circles c0 and c1.  side0 and side1 specify
    which side (LEFT or RIGHT) of c0 and c1 the tangent attaches to.  (LEFT
    and RIGHT from the perspective of c0 looking toward c1.)
    """

    # if we're not crossing over and the circles are the same size we need
    # to use a special method
    if side0 == side1 and c0.r == c1.r:
        return parallel_tangent(c0, c1, side0)

    # The following is based on math found here:
    # http://www.ambrsoft.com/TrigoCalc/Circles2/Circles2Tangent_.htm

    if side0 == side1:
        xp = ((c1.x * c0.r) - (c0.x * c1.r)) / (c0.r - c1.r)
        yp = ((c1.y * c0.r) - (c0.y * c1.r)) / (c0.r - c1.r)
    else:
        xp = ((c1.x * c0.r) + (c0.x * c1.r)) / (c0.r + c1.r)
        yp = ((c1.y * c0.r) + (c0.y * c1.r)) / (c0.r + c1.r)

    def root_part(xp, yp, x, y, r):
        return math.sqrt((xp - x)**2 + (yp - y)**2 - r**2)

    def denom_part(xp, yp, x, y):
        return (xp - x)**2 + (yp - y)**2

    root0 = root_part(xp, yp, c0.x, c0.y, c0.r)
    denom0 = denom_part(xp, yp, c0.x, c0.y)
    root1 = root_part(xp, yp, c1.x, c1.y, c1.r)
    denom1 = denom_part(xp, yp, c1.x, c1.y)

    sa = Segment(
        (c0.r**2 * (xp - c0.x) + c0.r * (yp - c0.y) * root0) / denom0 + c0.x,
        (c0.r**2 * (yp - c0.y) - c0.r * (xp - c0.x) * root0) / denom0 + c0.y,
        (c1.r**2 * (xp - c1.x) + c1.r * (yp - c1.y) * root1) / denom1 + c1.x,
        (c1.r**2 * (yp - c1.y) - c1.r * (xp - c1.x) * root1) / denom1 + c1.y,
    )
    sb = Segment(
        (c0.r**2 * (xp - c0.x) - c0.r * (yp - c0.y) * root0) / denom0 + c0.x,
        (c0.r**2 * (yp - c0.y) + c0.r * (xp - c0.x) * root0) / denom0 + c0.y,
        (c1.r**2 * (xp - c1.x) - c1.r * (yp - c1.y) * root1) / denom1 + c1.x,
        (c1.r**2 * (yp - c1.y) + c1.r * (xp - c1.x) * root1) / denom1 + c1.y,
    )

    if c0.r < c1.r and side0 == side1:
        if side0 == LEFT:
            s = sb
        elif side0 == RIGHT:
            s = sa
    else:
        if side0 == LEFT:
            s = sa
        elif side0 == RIGHT:
            s = sb

    return s

def det(v0, v1):
    return v0[0] * v1[1] - v0[1] * v1[0]

def dot(v0, v1):
    return v0[0] * v1[0] - v0[1] * v1[1]

def converging(near0, far0, near1, far1):
    """
    Determine whether the directional segments defined by near0 -> far0 and
    near1 -> far1 converge.

    Shorten the longer segment to match the shorter one (to avoid cross overs)
    then compare the distances between the endpoints.
    """
    v0 = sub_v(far0, near0)
    v1 = sub_v(far1, near1)

    near_distance = distance_v(near1, near0)
    if mag_v(v0) < mag_v(v1):
        shortened = add_v(
            scale_v(norm_v(v1), mag_v(v0)),
            near1
        )
        far_distance = distance_v(far0, shortened)
    else:
        shortened = add_v(
            scale_v(norm_v(v0), mag_v(v1)),
            near0
        )
        far_distance = distance_v(far1, shortened)

    return near_distance > far_distance

def arc(t0, t1, c, side):
    converges = converging(
        (t0.x1, t0.y1), (t0.x0, t0.y0),
        (t1.x0, t1.y0), (t1.x1, t1.y1),
    )

    return Arc(
        t0.x1, t0.y1, t1.x0, t1.y0, c.r, 0,
        l = 1 if converges else 0,
        s = 1 if side == LEFT else 0
    )

def arc_svg(a):
    return 'A {r} {r} {a} {l} {s} {x1} {y1}'.format(**a._asdict())

def tangent_svg(t):
    return 'L {x1} {y1}'.format(**t._asdict())

def draw_path(circles, sides):
    """
    Takes a list of N Circle objects and a list of N side constants (LEFT or
    RIGHT) and generates a path that traverses the circles as though it were a
    piece of string wrapped around them. The sides list determines which side of
    each circle the path passes by.

    More specifically, sides[i] dictates how the path passes around circle[i].
    """
    dwg = svgwrite.Drawing()
    tangents = [
        tangent(circles[i], circles[i+1], sides[i], sides[i+1])
        for i in range(len(circles) - 1)
    ] + [
        tangent(circles[-1], circles[0], sides[-1], sides[0])
    ]

    arcs = [
        arc(tangents[i-1], tangents[i], circles[i], sides[i])
        for i in range(len(tangents))
    ]

    path_commands = [ 'M {} {}'.format(arcs[0].x0, arcs[0].y0) ]
    for i in range(len(arcs)):
        path_commands.append(arc_svg(arcs[i]))
        path_commands.append(tangent_svg(tangents[i]))

    path = ' '.join(path_commands)

    svg_elements = [ dwg.path(path) ]

    for circle in circles:
        svg_elements.append(dwg.circle((circle.x, circle.y), circle.r, stroke='blue', fill_opacity=0))

    return svg_elements

def arm_circle(center, slope_v, length, radius):
    length_v = scale_v(norm_v(slope_v), length)
    total_v = add_v(length_v, center)

    return Circle(total_v[0], total_v[1], radius)

def slope_vector(degrees):
    rad = math.radians(degrees)
    return (round(math.sin(rad), 15), -round(math.cos(rad), 15))

def draw_arms(center, positions):
    """
    Draws an arm at ever position specified in positions.  Each position
    is an angle in degrees (0-359) clockwise from 12 o'clock.
    """
    circles = []
    sides = []

    for (i, position) in enumerate(positions):
        circles.append(arm_circle(center, slope_vector(position), 75, 10))
        sides.append(LEFT)

        # calculate armpit position
        if i + 1 == len(positions):
            delta = positions[0] +  (360 - position)
            armpit = ((delta / 2) + position) % 360
        else:
            delta = positions[i+1] - position
            armpit = (delta / 2) + position

        if delta >= 180:
            circles.append(arm_circle(center, (1, 0), 0, 15))
            sides.append(LEFT)
        else:
            circles.append(arm_circle(center, slope_vector(armpit), 35, 5))
            sides.append(RIGHT)

    return draw_path(circles, sides)

def draw_original():
    circles = [
        Circle(450, 100, 55), # UR
        Circle(108, 100, 55), # UL
        Circle(188, 100, 55),
        Circle(276, 120, 20),
        Circle(170, 425, 27), # LL
        Circle(310, 363, 38),
        Circle(318, 290, 33),
        Circle(370, 225, 26),
        Circle(620, 480, 35), # LR
    ]

    sides = [ RIGHT, RIGHT, RIGHT, LEFT, RIGHT, LEFT, RIGHT, LEFT, RIGHT ]
    return draw_path(circles, sides)

def main():
    """
    inspiration:
    http://www.dazeddigital.com/music/article/34849/1/aphex-twin-logo-designer-posts-early-blueprints-on-instagram

    language:
    - center circle
    - n arms on 3 axes
      - arm "end" circle always on axis
      - arm "pit" circle always somewhere between axes
      - complications between end and pit to one side of axis
    - always go right around the end and left around the pit
    - no overlapping circles when changing sides between them

    tooling:
    - find a point on an axis
    - find a point n units perpendicularly off the axis

    to do:
    X 3 arms, all the same length and width
    - random arms
    - random lengths and widths
    - slight angle variation
    - arm complications

    """
    scaling = 200
    svg_elements = []
    for center_y in range(scaling//2, scaling*4, scaling):
        for center_x in range(scaling//2, scaling*7, scaling):
            arms = [ random.randrange(0, 360, 10) for x in range(3) ]
            svg_elements += draw_arms((center_x, center_y), sorted(arms))

    dwg = svgwrite.Drawing('aphex.svg', profile='tiny')
    for svg_element in svg_elements:
        dwg.add(svg_element)
    dwg.save()

if __name__== "__main__":
    main()
