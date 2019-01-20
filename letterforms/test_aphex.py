import math
import unittest

import aphex

class TangentTest(unittest.TestCase):
    def test_inner(self):
        c0 = aphex.Circle(0, 0, 4)
        c1 = aphex.Circle(5, 5, 3)
        result_lr = aphex.tangent(c0, c1, aphex.LEFT, aphex.RIGHT)
        result_rl = aphex.tangent(c0, c1, aphex.RIGHT, aphex.LEFT)
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
        result_ll = aphex.tangent(c0, c1, aphex.LEFT, aphex.LEFT)
        result_rr = aphex.tangent(c0, c1, aphex.RIGHT, aphex.RIGHT)
        expected_ll = aphex.Segment(3.2, -2.4, 7.4, 3.2)
        expected_rr = aphex.Segment(-2.4, 3.2, 3.2, 7.4)
        self.assertEqual(result_ll, expected_ll)
        self.assertEqual(result_rr, expected_rr)

    def test_left_to_right(self):
        # c0 is bigger
        c0 = aphex.Circle(0, 0, 4)
        c1 = aphex.Circle(10, 0, 3)
        result_lr = aphex.tangent(c0, c1, aphex.LEFT, aphex.RIGHT)
        self.assertGreater(result_lr.y1, result_lr.y0)

        # c1 is bigger
        c0 = aphex.Circle(0, 0, 3)
        c1 = aphex.Circle(10, 0, 4)
        result_lr = aphex.tangent(c0, c1, aphex.LEFT, aphex.RIGHT)
        self.assertGreater(result_lr.y1, result_lr.y0)

    def test_right_to_left(self):
        # c0 is bigger
        c0 = aphex.Circle(0, 0, 4)
        c1 = aphex.Circle(10, 0, 3)
        result_rl = aphex.tangent(c0, c1, aphex.RIGHT, aphex.LEFT)
        self.assertGreater(result_rl.y0, result_rl.y1)

        # c1 is bigger
        c0 = aphex.Circle(0, 0, 3)
        c1 = aphex.Circle(10, 0, 4)
        result_rl = aphex.tangent(c0, c1, aphex.RIGHT, aphex.LEFT)
        self.assertGreater(result_rl.y0, result_rl.y1)

    def test_small_to_large(self):
        c0 = aphex.Circle(x=160, y=450, r=30)
        c1 = aphex.Circle(x=500, y=100, r=65)
        result = aphex.tangent(c0, c1, aphex.RIGHT, aphex.RIGHT)
        expected = aphex.Segment(
            x0=179.96358510145777,
            y0=472.3931969557018,
            x1=543.2544343864918,
            y1=148.51859340402063
        )
        self.assertEqual(result, expected)

    def test_outer_same_r(self):
        c0 = aphex.Circle(0, 0, 2)
        c1 = aphex.Circle(5, 5, 2)
        result_ll = aphex.tangent(c0, c1, aphex.LEFT, aphex.LEFT)
        result_rr = aphex.tangent(c0, c1, aphex.RIGHT, aphex.RIGHT)
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

    def test_converges(self):
        tin0 = (0, 0)
        tin1 = (2, 2)
        tout0 = (2, 3)
        tout1 = (0, 4)
        result = aphex.converging(tin1, tin0, tout0, tout1)
        self.assertFalse(result)

        tin0 = (2, 2)
        tin1 = (0, 0)
        tout0 = (0, 4)
        tout1 = (2, 3)
        result = aphex.converging(tin1, tin0, tout0, tout1)
        self.assertTrue(result)

class UtilTest(unittest.TestCase):
    def test_slope_vector(self):
        expected_vectors = [
            (0, (0.0, -1)),
            (45, (0.707106781186547, -0.707106781186548)),
            (90, (1.0, 0)),
            (135, (0.707106781186548, 0.707106781186547)),
            (180, (0.0, 1)),
            (225, (-0.707106781186547, 0.707106781186548)),
            (270, (-1.0, 0)),
            (315, (-0.707106781186548, -0.707106781186547)),
        ]
        for (angle, expected) in expected_vectors:
            self.assertEqual(aphex.slope_vector(angle), expected)

    def test_perp_slope_vector(self):
        expected_vectors = [
            (0, (1.0, 0)),
            (45, (0.707106781186548, 0.707106781186547)),
            (90, (0.0, 1)),
            (135, (-0.707106781186547, 0.707106781186548)),
            (180, (-1.0, 0)),
            (225, (-0.707106781186548, -0.707106781186547)),
            (270, (0.0, -1)),
            (315, (0.707106781186547, -0.707106781186548)),
        ]
        for (angle, expected) in expected_vectors:
            actual = aphex.slope_vector(angle, True)
            self.assertEqual(actual, expected)

    def test_spaced_out(self):
        threshold = 20
        tests = [
            ([0, 120, 240], True),
            ([0, 10, 20], False),
            ([0, 60, 359], False),
        ]
        for (positions, expected) in tests:
            self.assertEqual(
                aphex.spaced_out(positions, threshold),
                expected
            )

    def test_compute_center(self):
        tests = [
            (
                [
                    aphex.Circle(0, 0, 4),
                    aphex.Circle(5, 5, 3),
                ],
                (2.5, 2.5)
            ),
            (
                [
                    aphex.Circle(0, 0, 3),
                    aphex.Circle(5, 5, 3),
                    aphex.Circle(-5, -5, 3),
                ],
                (0, 0)
            ),
            (
                [
                    aphex.Circle(0, 0, 3),
                    aphex.Circle(6, 5, 3),
                    aphex.Circle(0, 1, 3),
                ],
                (2, 2)
            ),
        ]
        for (circles, expected) in tests:
            self.assertEqual(
                aphex.compute_center(circles),
                expected
            )

if __name__ == '__main__':
    unittest.main()
