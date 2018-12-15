import math
import unittest

import aphex

class BitangentTest(unittest.TestCase):
    def test_inner(self):
        result = aphex.bitangent(0, 0, 4, 5, 5, 3, True)
        expected = {
            'xp': 2.857142857142857,
            'yp': 2.857142857142857,
            'c0x0': 3.2,
            'c0y0': 2.4,
            'c0x1': 2.4,
            'c0y1': 3.2,
            'c1x0': 2.600000000000001,
            'c1y0': 3.1999999999999993,
            'c1x1': 3.1999999999999993,
            'c1y1': 2.600000000000001,
        }
        self.assertEqual(result, expected)

    def test_outer(self):
        result = aphex.bitangent(0, 0, 4, 5, 5, 3, False)
        expected = {
            'xp': 20.0,
            'yp': 20.0,
            'c0x0': 3.2,
            'c0y0': -2.4,
            'c0x1': -2.4,
            'c0y1': 3.2,
            'c1x0': 7.4,
            'c1y0': 3.2,
            'c1x1': 3.2,
            'c1y1': 7.4,
        }
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
