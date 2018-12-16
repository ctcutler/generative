import math
import unittest

import aphex

class BitangentTest(unittest.TestCase):
    def test_inner(self):
        c0 = aphex.Circle(0, 0, 4)
        c1 = aphex.Circle(5, 5, 3)
        result = aphex.bitangent(c0, c1, True)
        expected = {
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
        c0 = aphex.Circle(0, 0, 4)
        c1 = aphex.Circle(5, 5, 3)
        result = aphex.bitangent(c0, c1, False)
        expected = {
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

    def test_outer_same_r(self):
        c0 = aphex.Circle(0, 0, 2)
        c1 = aphex.Circle(5, 5, 2)
        result = aphex.bitangent(c0, c1, False)
        expected = {
            'c0x0': 1.414213562373095,
            'c0y0': -1.414213562373095,
            'c0x1': -1.414213562373095,
            'c0y1': 1.414213562373095,
            'c1x0': 6.414213562373095,
            'c1y0': 3.585786437626905,
            'c1x1': 3.585786437626905,
            'c1y1': 6.414213562373095,
        }
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
