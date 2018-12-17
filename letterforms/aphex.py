import collections
import math
import unittest

import svgwrite

Circle = collections.namedtuple('Circle', ['x', 'y', 'r'])
Segment = collections.namedtuple('Segment', ['x0', 'y0', 'x1', 'y1'])
LEFT = 'left'
RIGHT = 'right'

def mag_v(v):
    return math.sqrt(v[0]**2 + v[1]**2)

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

def bitangent(c0, c1, side0, side1):
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

    if side0 == LEFT and c0.r > c1.r:
        return Segment(
            (c0.r**2 * (xp - c0.x) + c0.r * (yp - c0.y) * root0) / denom0 + c0.x,
            (c0.r**2 * (yp - c0.y) - c0.r * (xp - c0.x) * root0) / denom0 + c0.y,
            (c1.r**2 * (xp - c1.x) + c1.r * (yp - c1.y) * root1) / denom1 + c1.x,
            (c1.r**2 * (yp - c1.y) - c1.r * (xp - c1.x) * root1) / denom1 + c1.y,
        )
    elif side0 == LEFT and c0.r <= c1.r:
        return Segment(
            (c0.r**2 * (xp - c0.x) - c0.r * (yp - c0.y) * root0) / denom0 + c0.x,
            (c0.r**2 * (yp - c0.y) + c0.r * (xp - c0.x) * root0) / denom0 + c0.y,
            (c1.r**2 * (xp - c1.x) - c1.r * (yp - c1.y) * root1) / denom1 + c1.x,
            (c1.r**2 * (yp - c1.y) + c1.r * (xp - c1.x) * root1) / denom1 + c1.y,
        )
    elif side0 == RIGHT and c0.r > c1.r:
        return Segment(
            (c0.r**2 * (xp - c0.x) - c0.r * (yp - c0.y) * root0) / denom0 + c0.x,
            (c0.r**2 * (yp - c0.y) + c0.r * (xp - c0.x) * root0) / denom0 + c0.y,
            (c1.r**2 * (xp - c1.x) - c1.r * (yp - c1.y) * root1) / denom1 + c1.x,
            (c1.r**2 * (yp - c1.y) + c1.r * (xp - c1.x) * root1) / denom1 + c1.y,
        )
    elif side0 == RIGHT and c0.r <= c1.r:
        return Segment(
            (c0.r**2 * (xp - c0.x) + c0.r * (yp - c0.y) * root0) / denom0 + c0.x,
            (c0.r**2 * (yp - c0.y) - c0.r * (xp - c0.x) * root0) / denom0 + c0.y,
            (c1.r**2 * (xp - c1.x) + c1.r * (yp - c1.y) * root1) / denom1 + c1.x,
            (c1.r**2 * (yp - c1.y) - c1.r * (xp - c1.x) * root1) / denom1 + c1.y,
        )

def arc_angle(pt0, pt1):
    #https://stackoverflow.com/questions/14066933/direct-way-of-computing-clockwise-angle-between-2-vectors/16544330#16544330
    dot = pt0[0] * pt1[0] + pt0[1] * pt1[1]
    det = pt0[0] * pt1[1] + pt0[1] * pt1[0]
    return math.degrees(math.atan2(dot, det))

def main():
    """
    http://www.dazeddigital.com/music/article/34849/1/aphex-twin-logo-designer-posts-early-blueprints-on-instagram

    two separate things:
    1) the description of the circles and the straight lines that connect them
    2) the lines and arcs that make up the path we build from 1)

    description
    - list of circles with radii and coordinates
    - list of tangents between those circles (just which side to which side)

    path components
    - based on description, build a list of tangents between circles
    - create corresponding list of arcs along circles between tangents
    - build path based on two lists

    """
    dwg = svgwrite.Drawing('aphex.svg', profile='tiny')
    c0 = Circle(100, 300, 50)
    c1 = Circle(300, 100, 25)
    c2 = Circle(500, 300, 50)

    for c in [c0, c1, c2]:
        dwg.add(dwg.circle((c.x, c.y), c.r, stroke='green', fill='white'))


    prev_end = None
    for (ca, cb) in [(c0, c1), (c1, c2), (c2, c0)]:
        left_left = bitangent(ca, cb, LEFT, LEFT)
        dwg.add(
            dwg.line(
                (left_left.x0, left_left.y0),
                (left_left.x1, left_left.y1),
                stroke='red'
            )
        )
        cur_start = (left_left.x0, left_left.y0)
        if prev_end:
            dwg.add(dwg.path(
                'M {} {} A {} {} {} {} {} {} {}'.format(
                    prev_end[0],
                    prev_end[1],
                    ca.r,
                    ca.r,
                    arc_angle(prev_end, cur_start),
                    0,
                    1,
                    cur_start[0],
                    cur_start[1]
                )
            ))
        prev_end = (left_left.x1, left_left.y1)

    dwg.save()

if __name__== "__main__":
    main()
