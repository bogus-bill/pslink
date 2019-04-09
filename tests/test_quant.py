import math
import unittest

import pslink.quant as quant


class TestQuantityModule(unittest.TestCase):

    def test_length_cm(self):
        self.assertAlmostEqual(
            quant.length_cm("some length in 42.42 inches"), 42.42 * 2.54)
        # should return the mean value
        cm = quant.length_cm("21.21 inches minimum and 42.42 inches maximum")
        self.assertAlmostEqual(cm, 2.54 * (21.21 + 42.42) / 2)

    def test_ring_volume(self):
        spec = """
        Cross-Sectional Shape Style              ; TEE
        Cross-Sectional Height                   ; 0.180 inches nominal
        Center Hole Diameter                     ; 1.106 inches nominal
        Peripheral Diameter                      ; 1.384 inches nominal
        End Item Identification                  ; F/A-18 E/F
        Criticality Code Justification           ; AGAV
        """
        bindings = {}
        for line in spec.strip().split("\n"):
            parts = line.split(";")
            bindings[parts[0].strip()] = parts[1].strip()
        vol_cm3 = quant.VolumeFormula.get_cm3(bindings)
        self.assertAlmostEqual(
            vol_cm3, (math.pi / 4) * 0.180 * (1.384**2 - 1.106**2) * 2.54**3)


if __name__ == "__main__":
    unittest.main()
