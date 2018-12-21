import collections
import math
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

    if side0 == LEFT:
        return Segment(
            (c0.r**2 * (xp - c0.x) + c0.r * (yp - c0.y) * root0) / denom0 + c0.x,
            (c0.r**2 * (yp - c0.y) - c0.r * (xp - c0.x) * root0) / denom0 + c0.y,
            (c1.r**2 * (xp - c1.x) + c1.r * (yp - c1.y) * root1) / denom1 + c1.x,
            (c1.r**2 * (yp - c1.y) - c1.r * (xp - c1.x) * root1) / denom1 + c1.y,
        )
    elif side0 == RIGHT:
        return Segment(
            (c0.r**2 * (xp - c0.x) - c0.r * (yp - c0.y) * root0) / denom0 + c0.x,
            (c0.r**2 * (yp - c0.y) + c0.r * (xp - c0.x) * root0) / denom0 + c0.y,
            (c1.r**2 * (xp - c1.x) - c1.r * (yp - c1.y) * root1) / denom1 + c1.x,
            (c1.r**2 * (yp - c1.y) + c1.r * (xp - c1.x) * root1) / denom1 + c1.y,
        )

def arc_angle(x0, y0, x1, y1):
    # from: https://stackoverflow.com/questions/14066933/direct-way-of-computing-clockwise-angle-between-2-vectors/16544330#16544330
    dot = x0 * x1 + y0 * y1
    det = x0 * y1 + y0 * x1
    return math.degrees(math.atan2(dot, det))

def arc(t0, t1, c, side):
    # large arc: arc is > 180 degrees
    # sweep: 
    angle = arc_angle(t0.x1, t0.y1, t1.x0, t1.y0)
    # arc 1: 0, 0 / 1, 0
    # arc 2: 0, 0
    # arc 3: 0, 1
    # arc 4: 1, 0
    # are the far parts of the tangents nearer or father away?
    # or: how do the slopes compare?. . . if they are equal then 
    # parallel. . . 

    # cannot brain this right now but suspect that I can use vector
    # arithmetic to tell whether vectors are diverging or converging
    # and *that* should tell me which sweep flag to use

    # subtract near points from far points and normalize
    v0 = sub_v((t0.x0, t0.y0), (t0.x1, t0.y1))
    v1 = sub_v((t1.x1, t1.y1), (t1.x0, t1.y0))

    print(v0)
    print(v1)
    print()

    d1 = distance_v(v1, v0) 

    doubled_v0 = scale_v(v0, 2)
    doubled_v1 = scale_v(v1, 2)

    d2 = distance_v(doubled_v1, doubled_v0)


    return Arc(
        t0.x1, t0.y1, t1.x0, t1.y0, c.r, angle,
        l = 1 if d2 < d1 else 0,
        s = 1 if side == LEFT else 0
    )

def arc_svg(a):
    return 'A {r} {r} {a} {l} {s} {x1} {y1}'.format(**a._asdict())

def tangent_svg(t):
    return 'L {x1} {y1}'.format(**t._asdict())

def draw(circles, sides):
    """
    Takes a list of N Circle objects and a list of N side constants (LEFT or
    RIGHT) and generates a path that traverses the circles as though it were a
    piece of string wrapped around them. The sides list determines which side of
    each circle the path passes by.

    More specifically, sides[i] dictates how the path passes around circle[i].
    """
    tangents = [
        tangent(circles[i], circles[i+1], sides[i], sides[i+1])
        for i in range(len(circles) - 1)
    ] + [
        tangent(circles[-1], circles[0], sides[-1], sides[0])
    ]

    arcs = [
        arc(tangents[-1], tangents[0], circles[0], sides[0])
    ] + [
        arc(tangents[i-1], tangents[i], circles[i], sides[i])
        for i in range(1, len(tangents))
    ]

    path_commands = [ 'M {} {}'.format(arcs[0].x0, arcs[0].y0) ]
    for i in range(len(tangents)):
        path_commands.append(arc_svg(arcs[i]))
        path_commands.append(tangent_svg(tangents[i]))

    path = ' '.join(path_commands)

    dwg = svgwrite.Drawing('aphex.svg', profile='tiny')
    dwg.add(dwg.path(path))

    for circle in circles:
        dwg.add(dwg.circle((circle.x, circle.y), circle.r, stroke='blue', fill_opacity=0))

    dwg.save()

def main():
    """
    http://www.dazeddigital.com/music/article/34849/1/aphex-twin-logo-designer-posts-early-blueprints-on-instagram
    """
    circles = [
        Circle(500, 100, 65),
        Circle(100, 100, 65),
        Circle(180, 100, 65),
        Circle(280, 124, 24),
    ]

    sides = [ RIGHT, RIGHT, RIGHT, LEFT ]

    draw(circles, sides)

if __name__== "__main__":
    main()
