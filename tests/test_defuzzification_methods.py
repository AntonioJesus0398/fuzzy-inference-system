import unittest
from src.membership_functions import triangular, trapezoidal
from src.classes import FuzzySet
from src.defuzzification import bisector_of_area, center_of_area, mean_of_maximum

A1 = FuzzySet('', triangular(1, 2, 3))
A2 = FuzzySet('', trapezoidal(0, 1, 2, 3))
class InferenceMethodsTestCase(unittest.TestCase):
    def test_boa(self):
        self.assertAlmostEqual(bisector_of_area(A1, 0.01, (1, 3)), 2.00, 2)

    def test_coa(self):
        self.assertAlmostEqual(center_of_area(A1, 0.5, (1, 3)), 2.00, 2)
    
    def test_mom(self):
        self.assertAlmostEqual(mean_of_maximum(A2, 0.2, (0, 3)), 1.50, 2)