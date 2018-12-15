import math
import unittest

import svgwrite

def root_part(xp, yp, x, y, r):
    return math.sqrt((xp - x)**2 + (yp - y)**2 - r**2)

def denom_part(xp, yp, x, y):
    return (xp - x)**2 + (yp - y)**2

def bitangent(x0, y0, r0, x1, y1, r1, inner):
    """
    Calculates the four inner or outer bitangent points between two circles
    defined by their center points and radiuses. See the unit tests for
    examples.

    Based on math found here:
    http://www.ambrsoft.com/TrigoCalc/Circles2/Circles2Tangent_.htm
    """

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
        'xp': xp,
        'yp': yp,

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
    """
    dwg = svgwrite.Drawing('aphex.svg', profile='tiny')
    circles = [
        (100, 100, 50),
        (300, 100, 50),
        (300, 300, 50),
    ]
    for c in circles:
        dwg.add(dwg.circle((c[0], c[1]), c[2], stroke='green', fill='white'))

    dwg.add(dwg.line((100, 50), (300, 50), stroke='blue'))
    dwg.save()

if __name__== "__main__":
    main()
