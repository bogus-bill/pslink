import unittest

import pslink.symap as symap


class SymapTest(unittest.TestCase):

    def test_stopwords(self):
        self.assertTrue(symap.is_stopword("at"))
        self.assertFalse(symap.is_stopword("steel"))

    def test_similarity(self):
        self.assertAlmostEqual(1.0, symap.similarity("steel", "steel"))
        self.assertAlmostEqual(0.0, symap.similarity("steel", "car"))

    def test_keywords(self):
        p = "Steel product, secondary structural, girts and purlins, at plant"
        expected = ["steel", "product", "secondary", "structural",
                    "girts", "purlins", "plant"]
        r = symap.keywords(p)
        self.assertEqual(len(r), len(expected))
        for e in expected:
            self.assertTrue(e in r)

    def test_best_match(self):
        match = symap.best_match("stainless steel", [
            "World Stainless Steel. 2005.  World Stainless Steel LCI",
            "Steel, stainless 304, quarto plate",
            "Stainless steel; Manufacture; Production mix, at plant; 316 2B"])
        self.assertEqual(match, "Steel, stainless 304, quarto plate")


if __name__ == "__main__":
    unittest.main()
