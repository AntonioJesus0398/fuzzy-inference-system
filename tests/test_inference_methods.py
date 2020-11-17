import unittest
from src.inference_methods import mamdani, larsen
from src.membership_functions import triangular, trapezoidal
from src.classes import FuzzySet, FuzzyRule, FuzzyRuleBase, LinguisticVariable

A1 = FuzzySet(triangular(1, 2, 4))
A2 = FuzzySet(triangular(0.5, 3, 5))

B1 = FuzzySet(triangular(0.6, 3, 5.4))
B2 = FuzzySet(triangular(0.5, 1, 2))

C1 = FuzzySet(triangular(1, 1.5, 3))
C2 = FuzzySet(triangular(0.2, 1, 1.2))

D1 = FuzzySet(triangular(1.2, 1.4, 2))
D2 = FuzzySet(triangular(0.5, 1.8, 2.1))

E1 = FuzzySet(triangular(1.2, 4, 4.5))
E2 = FuzzySet(triangular(1.3, 1, 1.5))

A = LinguisticVariable('A', {'A1': A1, 'A2': A2})
B = LinguisticVariable('B', {'B1': B1, 'B2': B2})
C = LinguisticVariable('C', {'C1': C1, 'C2': C2})
D = LinguisticVariable('D', {'D1': D1, 'D2': D2})
E = LinguisticVariable('E', {'E1': E1, 'E2': E2})

R1 = FuzzyRule(antecedent=[(A, 'A1'), (B, 'B1')], consequence=[(C, 'C1')])
R2 = FuzzyRule(antecedent=[(A, 'A2'), (B, 'B2')], consequence=[(C, 'C2')])

R_1 = FuzzyRule(antecedent=[(A, 'A1'), (B, 'B1'), (C, 'C1')], consequence=[(D, 'D1'), (E, 'E1')])
R_2 = FuzzyRule(antecedent=[(A, 'A2'), (B, 'B2'), (C, 'C2')], consequence=[(D, 'D2'), (E, 'E2')])


RB1 = FuzzyRuleBase()
RB1.add_rule(R1)
RB1.add_rule(R2)

RB2 = FuzzyRuleBase()
RB2.add_rule(R_1)
RB2.add_rule(R_2)

u, v, w = 3, 3.2, 2.5

class InferenceMethodsTestCase(unittest.TestCase):
    def test_mamdani_double_input_single_output(self):
        self.assertAlmostEqual(mamdani((u, v), RB1)['C'].membership_function(w).value, 0.33, 2)

    # def test_mamdani_multiple_input_single_output(self):
    #     print(mamdani((2.5, 3, 1.1), RB2))

    def test_larsen_double_input_single_output(self):
        self.assertAlmostEqual(larsen((u, v), RB1)['C'].membership_function(w).value, 0.17, 2)
