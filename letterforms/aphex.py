import collections
import math
import unittest

import svgwrite

Circle = collections.namedtuple('Circle', ['x', 'y', 'r'])
Segment = collections.namedtuple('Segment', ['x0', 'y0', 'x1', 'y1'])
LEFT = 'left'
RIGHT = 'right'

def norm_v(v):
    magnitude = math.sqrt(v[0]**2 + v[1]**2)
    return (v[0] / magnitude, v[1] / magnitude)

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

    if side0 == LEFT:
        return Segment(
            (c0.r**2 * (xp - c0.x) + c0.r * (yp - c0.y) * root0) / denom0 + c0.x,
            (c0.r**2 * (yp - c0.y) - c0.r * (xp - c0.x) * root0) / denom0 + c0.y,
            (c1.r**2 * (xp - c1.x) + c1.r * (yp - c1.y) * root1) / denom1 + c1.x,
            (c1.r**2 * (yp - c1.y) - c1.r * (xp - c1.x) * root1) / denom1 + c1.y,
        )
    else:
        return Segment(
            (c0.r**2 * (xp - c0.x) - c0.r * (yp - c0.y) * root0) / denom0 + c0.x,
            (c0.r**2 * (yp - c0.y) + c0.r * (xp - c0.x) * root0) / denom0 + c0.y,
            (c1.r**2 * (xp - c1.x) - c1.r * (yp - c1.y) * root1) / denom1 + c1.x,
            (c1.r**2 * (yp - c1.y) + c1.r * (xp - c1.x) * root1) / denom1 + c1.y,
        )


def main():
    """
    http://www.dazeddigital.com/music/article/34849/1/aphex-twin-logo-designer-posts-early-blueprints-on-instagram

    next steps:
    - create namedtuples for circles and tangents
    - figure out which tangent we want in any given circumstance and only
      ask for/receive it (lefts and rights are arbitrary right now)
    """
    dwg = svgwrite.Drawing('aphex.svg', profile='tiny')
    circles = [
        Circle(100, 100, 50),
        Circle(300, 100, 50),
        Circle(300, 300, 50),
    ]
    for c in circles:
        dwg.add(dwg.circle((c.x, c.y), c.r, stroke='green', fill='white'))


    left_left = bitangent(circles[0], circles[2], LEFT, LEFT)
    left_right = bitangent(circles[0], circles[2], LEFT, RIGHT)
    right_left = bitangent(circles[0], circles[2], RIGHT, LEFT)
    right_right = bitangent(circles[0], circles[2], RIGHT, RIGHT)
    dwg.add(
        dwg.line(
            (left_left.x0, left_left.y0),
            (left_left.x1, left_left.y1),
            stroke='red'
        )
    )
    dwg.add(
        dwg.line(
            (left_right.x0, left_right.y0),
            (left_right.x1, left_right.y1),
            stroke='red'
        )
    )
    dwg.add(
        dwg.line(
            (right_left.x0, right_left.y0),
            (right_left.x1, right_left.y1),
            stroke='blue'
        )
    )
    dwg.add(
        dwg.line(
            (right_right.x0, right_right.y0),
            (right_right.x1, right_right.y1),
            stroke='blue'
        )
    )

    dwg.save()

if __name__== "__main__":
    main()
