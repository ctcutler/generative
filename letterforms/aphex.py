import collections
import math
import unittest

import svgwrite

Circle = collections.namedtuple('Circle', ['x', 'y', 'r'])
Segment = collections.namedtuple('Segment', ['x0', 'y0', 'x1', 'y1'])

def root_part(xp, yp, x, y, r):
    return math.sqrt((xp - x)**2 + (yp - y)**2 - r**2)

def denom_part(xp, yp, x, y):
    return (xp - x)**2 + (yp - y)**2

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

def parallel_tangent(center_v1, center_v2, r, cw):
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

def parallel_tangents(x0, y0, x1, y1, r):
    center0 = (x0, y0)
    center1 = (x1, y1)
    c0t0 = parallel_tangent(center0, center1, r, False)
    c0t1 = parallel_tangent(center0, center1, r, True)
    c1t0 = parallel_tangent(center1, center0, r, True)
    c1t1 = parallel_tangent(center1, center0, r, False)

    return {
        'left': Segment(c0t0[0], c0t0[1], c1t0[0], c1t0[1]),
        'right': Segment(c0t1[0], c0t1[1], c1t1[0], c1t1[1]),
    }

def bitangent(c0, c1, inner):
    """
    Calculates the four inner or outer bitangent points between two circles
    defined by their center points and radiuses. See the unit tests for
    examples.

    Based on math found here:
    http://www.ambrsoft.com/TrigoCalc/Circles2/Circles2Tangent_.htm
    """

    # if we're doing outer tangents and the circles are the same size we need
    # to use a special method
    if not inner and c0.r == c1.r:
        return parallel_tangents(c0.x, c0.y, c1.x, c1.y, c0.r)

    if inner:
        xp = ((c1.x * c0.r) + (c0.x * c1.r)) / (c0.r + c1.r)
        yp = ((c1.y * c0.r) + (c0.y * c1.r)) / (c0.r + c1.r)
    else:
        xp = ((c1.x * c0.r) - (c0.x * c1.r)) / (c0.r - c1.r)
        yp = ((c1.y * c0.r) - (c0.y * c1.r)) / (c0.r - c1.r)

    root0 = root_part(xp, yp, c0.x, c0.y, c0.r)
    denom0 = denom_part(xp, yp, c0.x, c0.y)
    root1 = root_part(xp, yp, c1.x, c1.y, c1.r)
    denom1 = denom_part(xp, yp, c1.x, c1.y)

    return {
        'left': Segment(
            (c0.r**2 * (xp - c0.x) + c0.r * (yp - c0.y) * root0) / denom0 + c0.x,
            (c0.r**2 * (yp - c0.y) - c0.r * (xp - c0.x) * root0) / denom0 + c0.y,
            (c1.r**2 * (xp - c1.x) + c1.r * (yp - c1.y) * root1) / denom1 + c1.x,
            (c1.r**2 * (yp - c1.y) - c1.r * (xp - c1.x) * root1) / denom1 + c1.y,
        ),
        'right': Segment(
            (c0.r**2 * (xp - c0.x) - c0.r * (yp - c0.y) * root0) / denom0 + c0.x,
            (c0.r**2 * (yp - c0.y) + c0.r * (xp - c0.x) * root0) / denom0 + c0.y,
            (c1.r**2 * (xp - c1.x) - c1.r * (yp - c1.y) * root1) / denom1 + c1.x,
            (c1.r**2 * (yp - c1.y) + c1.r * (xp - c1.x) * root1) / denom1 + c1.y,
        ),
    }

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


    o = bitangent(circles[0], circles[2], False)
    i = bitangent(circles[0], circles[2], True)
    o_left = o['left']
    o_right = o['right']
    dwg.add(
        dwg.line(
            (o_left.x0, o_left.y0),
            (o_left.x1, o_left.y1),
            stroke='blue'
        )
    )
    dwg.add(
        dwg.line(
            (o_right.x0, o_right.y0),
            (o_right.x1, o_right.y1),
            stroke='blue'
        )
    )
    i_left = i['left']
    i_right = i['right']
    dwg.add(
        dwg.line(
            (i_left.x0, i_left.y0),
            (i_left.x1, i_left.y1),
            stroke='blue'
        )
    )
    dwg.add(
        dwg.line(
            (i_right.x0, i_right.y0),
            (i_right.x1, i_right.y1),
            stroke='blue'
        )
    )

    dwg.save()

if __name__== "__main__":
    main()
