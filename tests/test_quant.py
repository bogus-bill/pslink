import unittest

import pslink.quant as quant


class TestQuantityModule(unittest.TestCase):

    def test_length_cm(self):
        self.assertAlmostEqual(
            quant.length_cm("some length in 42.42 inches"), 42.42 * 2.54)
        # should return the mean value
        cm = quant.length_cm("21.21 inches minimum and 42.42 inches maximum")
        self.assertAlmostEqual(cm, 2.54 * (21.21 + 42.42) / 2)


if __name__ == "__main__":
    unittest.main()
