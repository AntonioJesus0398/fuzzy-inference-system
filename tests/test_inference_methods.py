import unittest
from src.inference_methods import mamdani, larsen
from src.membership_functions import triangular
from src.classes import FuzzySet, FuzzyRule

A1 = FuzzySet('', triangular(1, 2, 4))
A2 = FuzzySet('', triangular(0.5, 3, 5))

B1 = FuzzySet('', triangular(0.6, 3, 5.4))
B2 = FuzzySet('', triangular(0.5, 1, 2))

C1 = FuzzySet('', triangular(1, 1.5, 3))
C2 = FuzzySet('', triangular(0.2, 1, 1.2))

R1 = FuzzyRule((A1, B1), C1)
R2 = FuzzyRule((A2, B2), C2)

u, v, w = 3, 3.2, 2.5

class InferenceMethodsTestCase(unittest.TestCase):
    def test_mamdani(self):
        self.assertAlmostEqual(mamdani((u, v), [R1, R2]).membership_function(w).value, 0.33, 2)

    def test_larsen(self):
        self.assertAlmostEqual(larsen((u, v), [R1, R2]).membership_function(w).value, 0.17, 2)
