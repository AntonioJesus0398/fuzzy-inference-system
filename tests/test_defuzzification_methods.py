import unittest
from src.membership_functions import triangular
from src.classes import FuzzySet
from src.defuzzification import bisector_of_area

A1 = FuzzySet('', triangular(1, 2, 3))

class InferenceMethodsTestCase(unittest.TestCase):
    def test_boa(self):
        self.assertAlmostEquals(bisector_of_area(A1, 0.01, (1, 3)), 2.00, 2)
