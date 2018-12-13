import unittest

import numpy as np

import horizon1

class Horizon1Test(unittest.TestCase):
    def test_init_solid(self):
        result = horizon1.init_solid(3, 2, (0, 0, 255))
        expected = np.array([
            0, 0, 255, 0, 0, 255, 0, 0, 255,
            0, 0, 255, 0, 0, 255, 0, 0, 255,
        ]).reshape((2, 3, 3))
        np.testing.assert_equal(result, expected)

    def test_smooth_rands(self):
        result = horizon1.smooth_rands(10, 0, 5, .5, 12345)
        expected = np.array([2.164681, 2.081301, 1.59147, 1.916677, 1.715317,
            1.583728, 1.27739, 1.343398, 1.005086, 0.629353])
        np.testing.assert_allclose(result, expected, rtol=1e-05)

if __name__ == '__main__':
    unittest.main()
