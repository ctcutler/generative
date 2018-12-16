import math
import unittest

import aphex

class BitangentTest(unittest.TestCase):
    def test_inner(self):
        c0 = aphex.Circle(0, 0, 4)
        c1 = aphex.Circle(5, 5, 3)
        result = aphex.bitangent(c0, c1, True)
        expected = {
            'left': aphex.Segment(
                3.2, 2.4,
                2.600000000000001,
                3.1999999999999993,
            ),
            'right': aphex.Segment(
                2.4, 3.2,
                3.1999999999999993,
                2.600000000000001
            ),
        }
        self.assertEqual(result, expected)

    def test_outer(self):
        c0 = aphex.Circle(0, 0, 4)
        c1 = aphex.Circle(5, 5, 3)
        result = aphex.bitangent(c0, c1, False)
        expected = {
            'left': aphex.Segment(3.2, -2.4, 7.4, 3.2),
            'right': aphex.Segment(-2.4, 3.2, 3.2, 7.4)
        }
        self.assertEqual(result, expected)

    def test_outer_same_r(self):
        c0 = aphex.Circle(0, 0, 2)
        c1 = aphex.Circle(5, 5, 2)
        result = aphex.bitangent(c0, c1, False)
        expected = {
            'left': aphex.Segment(
                1.414213562373095,
                -1.414213562373095,
                6.414213562373095,
                3.585786437626905
            ),
            'right': aphex.Segment(
                -1.414213562373095,
                1.414213562373095,
                3.585786437626905,
                6.414213562373095
            )
        }
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
