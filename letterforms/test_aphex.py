import math
import unittest

import aphex

class BitangentTest(unittest.TestCase):
    def test_inner(self):
        c0 = aphex.Circle(0, 0, 4)
        c1 = aphex.Circle(5, 5, 3)
        result_lr = aphex.bitangent(c0, c1, aphex.LEFT, aphex.RIGHT)
        result_rl = aphex.bitangent(c0, c1, aphex.RIGHT, aphex.LEFT)
        expected_lr = aphex.Segment(
            3.2, 2.4,
            2.600000000000001,
            3.1999999999999993,
        )
        expected_rl = aphex.Segment(
            2.4, 3.2,
            3.1999999999999993,
            2.600000000000001
        )
        self.assertEqual(result_lr, expected_lr)
        self.assertEqual(result_rl, expected_rl)

    def test_outer(self):
        c0 = aphex.Circle(0, 0, 4)
        c1 = aphex.Circle(5, 5, 3)
        result_ll = aphex.bitangent(c0, c1, aphex.LEFT, aphex.LEFT)
        result_rr = aphex.bitangent(c0, c1, aphex.RIGHT, aphex.RIGHT)
        expected_ll = aphex.Segment(3.2, -2.4, 7.4, 3.2)
        expected_rr = aphex.Segment(-2.4, 3.2, 3.2, 7.4)
        self.assertEqual(result_ll, expected_ll)
        self.assertEqual(result_rr, expected_rr)

    def test_outer_same_r(self):
        c0 = aphex.Circle(0, 0, 2)
        c1 = aphex.Circle(5, 5, 2)
        result_ll = aphex.bitangent(c0, c1, aphex.LEFT, aphex.LEFT)
        result_rr = aphex.bitangent(c0, c1, aphex.RIGHT, aphex.RIGHT)
        expected_ll = aphex.Segment(
            1.414213562373095,
            -1.414213562373095,
            6.414213562373095,
            3.585786437626905
        )
        expected_rr = aphex.Segment(
            -1.414213562373095,
            1.414213562373095,
            3.585786437626905,
            6.414213562373095
        )
        self.assertEqual(result_ll, expected_ll)
        self.assertEqual(result_rr, expected_rr)

if __name__ == '__main__':
    unittest.main()
