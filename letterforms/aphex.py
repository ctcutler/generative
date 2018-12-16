import math
import unittest

import svgwrite

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
        'c0x0': c0t0[0],
        'c0y0': c0t0[1],
        'c0x1': c0t1[0],
        'c0y1': c0t1[1],

        'c1x0': c1t0[0],
        'c1y0': c1t0[1],
        'c1x1': c1t1[0],
        'c1y1': c1t1[1],
    }

def bitangent(x0, y0, r0, x1, y1, r1, inner):
    """
    Calculates the four inner or outer bitangent points between two circles
    defined by their center points and radiuses. See the unit tests for
    examples.

    Based on math found here:
    http://www.ambrsoft.com/TrigoCalc/Circles2/Circles2Tangent_.htm
    """

    # if we're doing outer tangents and the circles are the same size we need
    # to use a special method
    if not inner and r0 == r1:
        return parallel_tangents(x0, y0, x1, y1, r0)

    if inner:
        xp = ((x1 * r0) + (x0 * r1)) / (r0 + r1)
        yp = ((y1 * r0) + (y0 * r1)) / (r0 + r1)
    else:
        xp = ((x1 * r0) - (x0 * r1)) / (r0 - r1)
        yp = ((y1 * r0) - (y0 * r1)) / (r0 - r1)

    root0 = root_part(xp, yp, x0, y0, r0)
    denom0 = denom_part(xp, yp, x0, y0)
    root1 = root_part(xp, yp, x1, y1, r1)
    denom1 = denom_part(xp, yp, x1, y1)

    return {
        'c0x0': (r0**2 * (xp - x0) + r0 * (yp - y0) * root0) / denom0 + x0,
        'c0y0': (r0**2 * (yp - y0) - r0 * (xp - x0) * root0) / denom0 + y0,
        'c0x1': (r0**2 * (xp - x0) - r0 * (yp - y0) * root0) / denom0 + x0,
        'c0y1': (r0**2 * (yp - y0) + r0 * (xp - x0) * root0) / denom0 + y0,

        'c1x0': (r1**2 * (xp - x1) + r1 * (yp - y1) * root1) / denom1 + x1,
        'c1y0': (r1**2 * (yp - y1) - r1 * (xp - x1) * root1) / denom1 + y1,
        'c1x1': (r1**2 * (xp - x1) - r1 * (yp - y1) * root1) / denom1 + x1,
        'c1y1': (r1**2 * (yp - y1) + r1 * (xp - x1) * root1) / denom1 + y1,
    }

def main():
    """
    http://www.dazeddigital.com/music/article/34849/1/aphex-twin-logo-designer-posts-early-blueprints-on-instagram

    next steps:
    - create namedtuples for circles and tangents
    - figure out which tangent we want in any given circumstance and only
      ask for/receive it
    """
    dwg = svgwrite.Drawing('aphex.svg', profile='tiny')
    circles = [
        (100, 100, 50),
        (300, 100, 50),
        (300, 300, 50),
    ]
    for c in circles:
        dwg.add(dwg.circle((c[0], c[1]), c[2], stroke='green', fill='white'))


    o = bitangent(100, 100, 50, 300, 300, 50, False)
    i = bitangent(100, 100, 50, 300, 300, 50, True)
    dwg.add(
        dwg.line((o['c0x0'], o['c0y0']), (o['c1x0'], o['c1y0']), stroke='blue')
    )
    dwg.add(
        dwg.line((o['c0x1'], o['c0y1']), (o['c1x1'], o['c1y1']), stroke='blue')
    )
    dwg.add(
        dwg.line((i['c0x0'], i['c0y0']), (i['c1x0'], i['c1y0']), stroke='blue')
    )
    dwg.add(
        dwg.line((i['c0x1'], i['c0y1']), (i['c1x1'], i['c1y1']), stroke='blue')
    )

    dwg.save()

if __name__== "__main__":
    main()
