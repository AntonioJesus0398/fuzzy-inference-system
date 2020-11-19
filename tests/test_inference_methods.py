import unittest
from src.inference_methods import aggregate
from src.membership_functions import triangular, trapezoidal, singleton
from src.classes import FuzzySet, FuzzyRule, FuzzyRuleBase, LinguisticVariable

A = LinguisticVariable('A', (0.5, 3))
A1 = triangular(0.5, 1, 2)
A2 = triangular(1, 1.2, 3)
A.add_term('A1', A1)
A.add_term('A2', A2)

B = LinguisticVariable('B', (0, 4))
B1 = triangular(1, 2, 4)
B2 = triangular(0, 2.2, 3)
B.add_term('B1', B1)
B.add_term('B2', B2)

C = LinguisticVariable('C', domain=(0.5, 4))
C1 = triangular(0.5, 3, 4)
C2 = triangular(1, 2, 3)
C.add_term('C1', C1)
C.add_term('C2', C2)

RB = FuzzyRuleBase((A, B), (C,))
RB.add_rule([('A', 'A1'), ('B', 'B1')], [('C', 'C1')])
RB.add_rule([('A', 'A2'), ('B', 'B2')], [('C', 'C2')])

A_ = FuzzySet(triangular(0.5, 1, 1.5), domain=(0.5, 3))
B_ = FuzzySet(triangular(0.1, 1, 2), domain=(0, 4))

class InferenceMethodsTestCase(unittest.TestCase):
    def test_mamdani(self):
        result = aggregate((A_, B_), RB, step=0.001)
        self.assertAlmostEqual(result['C'].membership_function(2.5).value, 0.5, 2)
        self.assertAlmostEqual(result['C'].membership_function(3.1).value, 0.5, 2)
    
    def test_larsen(self):
        result = aggregate((A_, B_), RB, method="Larsen", step=0.001)
        self.assertAlmostEqual(result['C'].membership_function(2.5).value, 0.4, 2)
        self.assertAlmostEqual(result['C'].membership_function(3.1).value, 0.45, 2)


